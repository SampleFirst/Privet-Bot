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
        await message.reply_text("Please provide a movie name to search.")
        return
    query = query[1]
    search_results = await message.reply_text("Processing...")
    cine_list = search_movies(query)
    if cine_list:
        keyboards = []
        for movie in cine_list:
            keyboard = [InlineKeyboardButton(movie["title"], callback_data=movie["id"])]
            keyboards.append(keyboard)
        reply_markup = InlineKeyboardMarkup(keyboards)
        await search_results.edit_text('Search Results...', reply_markup=reply_markup)
    else:
        await search_results.edit_text('Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.')


@Client.on_callback_query(filters.regex('^link'))
async def movie_result(client, callback_query):
    query = callback_query
    movie_id = query.data
    s = get_movie(cine_list[movie_id])
    links = s["links"]
    caption = f"🎥 {s['title']}\n\n⚡ Download Links:\n"
    for name, link in links.items():
        caption += f"{name}: {link}\n"
    await query.message.reply_text(caption)
    await query.answer("Sent movie links")


def search_movies(query):
    cine_list = []
    cines_details = {}
    website = requests.get(f"https://1cinevood.site/?s={query.replace(' ', '+')}")
    if website.status_code == 200:
        website = website.text
        website = BeautifulSoup(website, "html.parser")
        movies = website.find_all("a", {'class': 'post-image post-image-left'})
        for movie in movies:
            if movie:
                cines_details["id"] = f"link{movies.index(movie)}"
                cines_details["title"] = movie.find('img')['alt']
                cine_list[cines_details["id"]] = movie['href']
                print(movie['href'])
                cine_list.append(cines_details)
                cines_details = {}
    return cine_list

def get_movie(movie_page_url):
    cine_details = {}
    cine_page = requests.get(movie_page_url)
    if cine_page.status_code == 200:
        cine_page = cine_page.text
        cine_page = BeautifulSoup(cine_page, "html.parser")
        title = cine_page.find_all("a", {'class': 'glow-on-hover'})
        cine_details["title"] = title
        links = title.find_all("a", {'rel': 'noopener', 'target': '_blank'})
        final_links = {}
        for i in links:
            final_links[f"{i.text}"] = i['href']
        cine_details["links"] = final_links
    return cine_details
