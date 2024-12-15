from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
from info import ADMINS  # Assuming ADMINS is defined in the `info` module.

cine_list = {}

@Client.on_message(filters.command("cinevood") & filters.user(ADMINS))
async def cinevood(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) == 1:
        await message.reply_text("Please provide a name to search.")
        return

    query = query[1]
    search_results = await message.reply_text("Processing...")
    movies_list = search_movies(query)

    if movies_list:
        keyboards = []
        for movie in movies_list:
            keyboard = [InlineKeyboardButton(movie["title"], callback_data=movie["id"])]
            keyboards.append(keyboard)
        reply_markup = InlineKeyboardMarkup(keyboards)
        await search_results.edit_text("Search Results:", reply_markup=reply_markup)
    else:
        await search_results.edit_text("Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.")

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
            # Extract all URLs within the `style` attribute
            urls = [url.strip() for url in style.split("url(") if ")" in url]
            if len(urls) > 1:  # Assuming the second URL is the poster
                poster_url = urls[1].split(")")[0]
                movie_details["poster"] = poster_url
            else:
                movie_details["poster"] = None
        else:
            movie_details["poster"] = None

        # Extract download links
        download_links = soup.find_all("a", {"class": "maxbutton-2 maxbutton maxbutton-filepress"})
        final_links = []

        for download_link in download_links:
            link_text_tag = download_link.find("span", {"class": "mb-text"})
            link_text = link_text_tag.text.strip() if link_text_tag else "Unnamed Link"

            href = download_link.get("href")
            if href:
                final_links.append({"name": link_text, "url": href})

        movie_details["links"] = final_links

    else:
        movie_details["error"] = f"Failed to fetch the page. Status code: {response.status_code}"

    return movie_details
