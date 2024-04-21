# skylatest.py
import asyncio
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from info import ADMINS, LOG_CHANNEL


@Client.on_message(filters.command("cinetranding"))
async def cine_tranding_movies(client, message):
    msg = await message.reply_text("Fetching popular movies...", quote=True)
    url = f"https://1cinevood.site/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.find_all('div', {'class': 'swiper-slide'})
        movie_list = ""
        for movie in movies:
            movie_list += f"<code>{movie}</code>\n\n"

        await msg.delete()
        main = await message.reply_text(f"Most Popular Movies:\n\n{movie_list}", quote=True)
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"Latest Updated Movies:\n\n{movie_list}"
        )
        
        await asyncio.sleep(15)
        await main.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")


@Client.on_message(filters.command("cinelatest"))
async def cine_latest_movies(client, message):
    msg = await message.reply_text("Fetching latest movies...", quote=True)
    url = f"https://1cinevood.site/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extracting only the relevant movie information
        movies = soup.find('h2', {'class': 'title front-view-title'})
        movie_list = ""
        for movie in movies:
            movie_list += f"<code>{movie}</code>\n\n"
        
        await msg.delete()
        main = await message.reply_text(f"Latest Updated Movies:\n\n{movie_list}", quote=True)
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"Latest Updated Movies:\n\n{movie_list}"
        )
        
        await asyncio.sleep(15)
        await main.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        
