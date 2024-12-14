from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from info import ADMINS 

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
        await search_results.edit_text('Search Results...', reply_markup=reply_markup)
    else:
        await search_results.edit_text('Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.')

@Client.on_callback_query(filters.regex('^cine'))
async def movie_result(client, callback_query):
    query = callback_query
    movie_id = query.data
    s = get_movie(cine_list[movie_id])

    # Prepare a list of links
    links = s["links"]
    links_list = "\n".join(
        [f"{idx + 1}. [{link['name']}]({link['url']})" for idx, link in enumerate(links)]
    )

    # Prepare the caption with the list of links
    caption = f"🎥 **{s['title']}**\n\n⚡ **Download Links:**\n{links_list}"

    # Send the formatted message
    await query.message.reply_text(
        caption, 
        parse_mode="Markdown", 
        disable_web_page_preview=True
    )
    await query.answer("Sent movie links")

def search_movies(query):
    movies_list = []
    movies_details = {}
    website = requests.get(f"https://1cinevood.digital/?s={query.replace(' ', '+')}")
    if website.status_code == 200:
        website = website.text
        website = BeautifulSoup(website, "html.parser")
        movies = website.find_all("a", {'class': 'post-image post-image-left'})
        for movie in movies:
            if movie:
                movies_details["id"] = f"cine{movies.index(movie)}"
                movies_details["title"] = movie.find('img')['alt']
                cine_list[movies_details["id"]] = movie['href']
                movies_list.append(movies_details)
                movies_details = {}
    return movies_list

def get_movie(movie_page_url):
    # Initialize an empty dictionary to store movie details
    movie_details = {}

    # Fetch the HTML content of the movie page
    response = requests.get(movie_page_url)
    if response.status_code == 200:  # Ensure the request was successful
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the movie title
        title = soup.find("div", {'class': 'title single-title entry-title'})
        movie_details["title"] = title.text.strip() if title else "No title found"

        # Extract download buttons and links
        download_buttons = soup.find_all("div", {'class': 'download-btns'})
        final_links = []

        for button in download_buttons:
            button_links = button.find_all("a")  # Find all <a> tags inside the button
            for link in button_links:
                # Extract button name and URL
                button_name = link.text.strip()
                button_url = link["href"]
                final_links.append({"name": button_name, "url": button_url})

        movie_details["links"] = final_links  # Store all button links

    return movie_details

