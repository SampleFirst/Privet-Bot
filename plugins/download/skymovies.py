# skymovies.py 
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from bs4 import BeautifulSoup
from info import ADMINS, LOG_CHANNEL 
import tldextract
from urllib.parse import urlparse
from database.domain_db import dm  
from plugins.download.domain import fetch_new_domain, fetch_new_suffix


movie_links = {}
group_links = {}

@Client.on_message(filters.command("skymovies") & filters.user(ADMINS))
async def skymovieshd(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) == 1:
        await message.reply_text("Please provide a movie name to search.")
        return
    query = query[1]
    search_results = await message.reply_text(f"Searching for *{query}*...")
    try:
        site = await fetch_new_domain()
        latest_domain = await dm.get_latest_domain(site)
        movies_list = search_movies(query, latest_domain)
        if movies_list:
            count = len(movies_list)
            keyboards = []
            for movie in movies_list:
                keyboard = [InlineKeyboardButton(movie["title"], callback_data=movie["id"])]
                keyboards.append(keyboard)
            reply_markup = InlineKeyboardMarkup(keyboards)
            await search_results.edit_text(f'Search Results found: {count}\n\nChoose a movie from *{query}*:', reply_markup=reply_markup)
        else:
            await search_results.edit_text(f'Sorry 🙏, No results found for *{query}*.\nCheck if you have misspelled the movie name.')
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex('^app\d+$'))
async def movie_result(client, callback_query):
    try:
        query = callback_query
        movie_id = query.data
        site = await fetch_new_domain()
        latest_domain = await dm.get_latest_domain(site)
        group_list = get_movie(movie_links[movie_id], latest_domain)
        if group_list:
            keyboards = []
            for group in group_list:
                keyboard = [InlineKeyboardButton(group["title"], callback_data=group["id"])]
                keyboards.append(keyboard)
            reply_markup = InlineKeyboardMarkup(keyboards)
            await query.answer("Showing groups...")
            await query.message.reply_text(f"Choose a group for *{movie_links[movie_id]}*:", reply_markup=reply_markup)
        else:
            await query.message.reply_text("No group finals available for this movie.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred: {str(e)}")

@Client.on_callback_query(filters.regex('^pay\d+$'))
async def final_movies_result(client, callback_query):
    try:
        query = callback_query
        group_id = query.data
        finale_list = final_page(group_links[group_id])
        if finale_list:
            links = finale_list["links"]
            response_text = ""
            for title, url in links.items():
                x = urlparse(url).netloc
                domain = f"<code>{x}</code>"
                response_text += f"Title: {domain}\nUrl: {url}\n\n"
            await query.message.reply_text(
                text=response_text,
                disable_web_page_preview=True
            )
            await query.answer("Sent movie links")
        else:
            await query.message.reply_text("No download links available for this movie.")
    except Exception as e:
        await query.message.reply_text(f"An error occurred: {str(e)}")

# @Client.on_callback_query(filters.regex('^pay\d+$'))
# async def final_movies_result(client, callback_query):
    # try:
        # query = callback_query
        # group_id = query.data
        # finale_list = final_page(group_links[group_id])
        # if finale_list:
            # link_buttons = []
            # links = finale_list["links"]
            # for name, link in links.items():
                # ext = tldextract.extract(link)
                # domain = ext.domain
                # suffix = ext.suffix
                # button = InlineKeyboardButton(f"{domain}.{suffix}", url=link)
                # link_buttons.append([button])
            # reply_markup = InlineKeyboardMarkup(link_buttons)
            # await query.message.reply_text("Click on the below buttons to download:", reply_markup=reply_markup)
            # await query.answer("Sent movie links")
        # else:
            # await query.message.reply_text("No download links available for this movie.")
    # except Exception as e:
        # await query.message.reply_text(f"An error occurred: {str(e)}")

def search_movies(query, latest_domain):
    movies_list = []
    try:
        website = requests.get(f"https://{latest_domain}/search.php?search={query.replace(' ', '+')}&cat=All")
        if website.status_code == 200:
            website = website.text
            website = BeautifulSoup(website, "html.parser")
            movies = website.find_all("div", {'class': 'L'})
            for movie in movies:
                movie_details = {}
                movie_link = movie.find("a", href=True)
                if movie_link:
                    movie_details["id"] = f"app{movies.index(movie)}"
                    movie_details["title"] = movie_link.text.strip()
                    movie_links[movie_details["id"]] = movie_link['href']
                    movies_list.append(movie_details)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return movies_list

def get_movie(movie_page_url, latest_domain):
    group_list = []
    try:
        movie_page = f"https://{latest_domain}" + movie_page_url
        webpage = requests.get(movie_page)
        if webpage.status_code == 200:
            webpage = webpage.text
            webpage = BeautifulSoup(webpage, "html.parser")
            groups = webpage.find("div", {'class': 'Bolly'})
            if groups:
                groups = groups.find_all("a", href=True)
                for group in groups:
                    group_details = {}
                    group_details["id"] = f"pay{groups.index(group)}"
                    group_details["title"] = group.text.strip()
                    group_links[group_details["id"]] = group['href']
                    group_list.append(group_details)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return group_list

def final_page(final_page_url):
    finale_list = {}
    try:
        final_page = final_page_url
        webpage = requests.get(final_page)
        if webpage.status_code == 200:
            webpage = webpage.text
            webpage = BeautifulSoup(webpage, 'html.parser')
            links = webpage.find_all("a", {'rel': 'external'})
            final_links = {}
            for link in links:
                final_links[f"{link.text}"] = link['href']
            finale_list["links"] = final_links
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    return finale_list
