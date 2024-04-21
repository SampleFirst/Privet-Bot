import asyncio
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from info import ADMINS, LOG_CHANNEL

@Client.on_message(filters.command("cinetrending"))
async def cine_trending(client, message):
    try:
        msg = await message.reply_text("Fetching trending movies...", quote=True)
        url = "https://1cinevood.site/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        trending_movies = []
        movie_containers = soup.find_all('div', class_='box-in')
        for container in movie_containers:
            title = container.find('a')['title']
            trending_movies.append(title)

        message_text = "Trending Movies:\n\n" + "\n".join([f"<code>{movie}</code>" for movie in trending_movies])
        await msg.edit_text(message_text)
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=message_text
        )
        await asyncio.sleep(15)
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@Client.on_message(filters.command("cinelatest"))
async def cine_latest(client, message):
    try:
        msg = await message.reply_text("Fetching latest movies...", quote=True)
        url = f"https://1cinevood.site/"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extracting only the relevant movie information
        movies = soup.find_all('h2', {'class': 'title front-view-title'})
        movie_list = "\n".join([f"<code>{movie.text}</code>" for movie in movies])
        
        await msg.edit_text(f"Latest Updated Movies:\n\n{movie_list}")
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"Latest Updated Movies:\n\n{movie_list}"
        )
        
        await asyncio.sleep(15)
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
