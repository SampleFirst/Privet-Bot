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
    link_buttons = []
    links = s["links"]
    for link in links:
        button = InlineKeyboardButton(link["name"], url=link["url"])
        link_buttons.append([button])

    caption = f"🎥 {s['title']}\n\n⚡ Download Links:"
    reply_markup = InlineKeyboardMarkup(link_buttons)

    await query.message.reply_text(caption, reply_markup=reply_markup)
    await query.answer("Sent movie links")

def search_movies(query):
    movies_list = []
    movies_details = {}
    website = requests.get(f"https://1cinevood.site/?s={query.replace(' ', '+')}")
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
    movie_details = {}
    movie_page_link = requests.get(movie_page_url)
    if movie_page_link.status_code == 200:
        movie_page_link = movie_page_link.text
        movie_page_link = BeautifulSoup(movie_page_link, "html.parser")
        title = movie_page_link.find("div", {'class': 'title single-title entry-title'})
        movie_details["title"] = title
        download_links = movie_page_link.find_all("div", {'class': 'download-btns'})
        final_links = []
        for download_link in download_links:
            link_text = download_link.find("h6").text.strip()
            links = download_link.find_all("a")
            for link in links:
                final_links.append({"name": link_text, "url": link["href"]})
        movie_details["links"] = final_links
    return movie_details
    
