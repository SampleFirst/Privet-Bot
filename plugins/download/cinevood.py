from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
from utils import temp, check_verification, get_token
from info import ADMINS, IS_VERIFY, HOW_TO_VERIFY

cine_list = {}

@Client.on_message(filters.command("cinevood") & filters.user(ADMINS))
async def cinevood(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) == 1:
        await message.reply_text("Please provide a name to search.")
        return

    search_query = query[1]
    search_results = await message.reply_text("Processing...")

    if IS_VERIFY:
        user_id = message.from_user.id
        if not await check_verification(client, user_id):
            btn = [
                [
                    InlineKeyboardButton(
                        "Verify",
                        url=await get_token(
                            client,
                            user_id,
                            f"https://telegram.me/{temp.U_NAME}?start="
                        )
                    ),
                    InlineKeyboardButton("How To Verify", url=HOW_TO_VERIFY)
                ]
            ]
            await search_results.edit_text(
                chat_id=user_id,
                text=(
                    "<b>You are not verified!\n"
                    "Kindly verify to continue so you can get access to unlimited movies "
                    "for the next 12 hours!</b>"
                ),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(btn),
                protect_content=False
            )
            return
    # Search movies and generate response
    movies_list = search_movies(search_query)
    if movies_list:
        keyboards = [
            [InlineKeyboardButton(movie["title"], callback_data=movie["id"])]
            for movie in movies_list
        ]
        reply_markup = InlineKeyboardMarkup(keyboards)
        await search_results.edit_text("Search Results:", reply_markup=reply_markup)
    else:
        await search_results.edit_text(
            "Sorry 🙏, no results found!\n"
            "Check if you have misspelled the movie name."
        )
        
@Client.on_callback_query(filters.regex("^cine"))
async def movie_result(client, callback_query):
    movie_id = callback_query.data
    if movie_id not in cine_list:
        await callback_query.answer("Movie not found!", show_alert=True)
        return

    movie_data = get_movie(cine_list[movie_id])

    if "error" in movie_data:
        await callback_query.answer(movie_data["error"], show_alert=True)
        return

    link_buttons = [
        [InlineKeyboardButton(link["name"], url=link["url"])]
        for link in movie_data["links"]
    ]

    caption = f"🎥 **{movie_data['title']}**\n\n⚡ **Download Links:**"
    reply_markup = InlineKeyboardMarkup(link_buttons)

    poster_url = movie_data.get("poster", None)
    if poster_url:
        await callback_query.message.reply_photo(
            photo=poster_url,
            caption=caption,
            reply_markup=reply_markup,
        )
    else:
        await callback_query.message.reply_text(
            caption,
            reply_markup=reply_markup,
        )

    await callback_query.answer("Sent movie links!")

def search_movies(query):
    movies_list = []
    website = requests.get(f"https://1cinevood.digital/?s={query.replace(' ', '+')}")

    if website.status_code == 200:
        soup = BeautifulSoup(website.text, "html.parser")
        movies = soup.find_all("a", {"class": "post-image post-image-left"})

        for index, movie in enumerate(movies):
            if movie:
                movie_details = {
                    "id": f"cine{index}",
                    "title": movie.find("img")["alt"],
                }
                cine_list[movie_details["id"]] = movie["href"]
                movies_list.append(movie_details)
    return movies_list


def get_movie(movie_page_url):
    movie_details = {}
    response = requests.get(movie_page_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract the movie title
        title_tag = soup.find("title")
        movie_details["title"] = title_tag.text.strip() if title_tag else "Title not found"

        # Extract the poster URL from the `style` attribute
        poster_tag = soup.find("div", {"class": "poster_parent"})
        if poster_tag and "style" in poster_tag.attrs:
            style = poster_tag["style"]
            # Extract URLs within the `style` attribute
            urls = [url.strip() for url in style.split("url(") if ")" in url]
            if len(urls) > 1:  # Assuming the second URL is the poster
                poster_url = urls[1].split(")")[0]
                movie_details["poster"] = poster_url
            else:
                movie_details["poster"] = None
        else:
            movie_details["poster"] = None

        # Extract download links and associated details
        download_links = soup.find_all("a", {"class": "maxbutton-2 maxbutton maxbutton-filepress"})
        final_links = []

        for download_link in download_links:
            # Find the closest preceding <h6><span> for movie details
            details_tag = download_link.find_previous("h6").find("span")
            link_text = details_tag.text.strip() if details_tag else "Unnamed Link"

            # Extract the href (URL) from the link
            href = download_link.get("href")
            if href:
                final_links.append({
                    "name": link_text,
                    "url": href
                })

        movie_details["links"] = final_links

    else:
        movie_details["error"] = f"Failed to fetch the page. Status code: {response.status_code}"

    return movie_details
