from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
import re
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
            urls = [url.strip() for url in style.split("url(") if ")" in url]
            movie_details["poster"] = urls[1].split(")")[0] if len(urls) > 1 else None
        else:
            movie_details["poster"] = None

        # Extract download links
        download_sections = soup.find_all("a", {"class": "maxbutton-2 maxbutton maxbutton-filepress"})
        final_links = []

        for download_section in download_sections:
            # Extract link URL
            href = download_section.get("href")
            if not href:
                continue

            # Extract size and resolution from parent text
            parent_text = download_section.find_parent("div").get_text(strip=True)
            resolution = extract_resolution(parent_text)
            file_size = extract_file_size(parent_text)

            # Create a meaningful button text with ✅
            button_text = f"✅ {resolution} ({file_size})" if resolution and file_size else "✅ FilePress"
            button_text = truncate_text(button_text)  # Truncate if too long

            final_links.append({"name": button_text, "url": href})

        movie_details["links"] = final_links

    else:
        movie_details["error"] = f"Failed to fetch the page. Status code: {response.status_code}"

    return movie_details

def extract_file_size(text):
    """Extract file size (e.g., 5.33 GB, 456 MB) from text."""
    match = re.search(r"(\d+(\.\d+)?\s?(GB|MB))", text, re.IGNORECASE)
    return match.group(0) if match else "Unknown Size"

def extract_resolution(text):
    """Extract resolution (e.g., 480p, 720p, 1080p) from text."""
    match = re.search(r"(\d{3,4}p)", text)
    return match.group(0) if match else "Unknown Resolution"

def truncate_text(text, max_length=64):
    """Truncate text to fit Telegram button limits."""
    return text if len(text) <= max_length else text[:61] + "..."
