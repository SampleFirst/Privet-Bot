# skylatest.py
import asyncio
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from info import ADMINS, LOG_CHANNEL


def get_trending_movies():
    url = "https://1cinevood.site/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    trending_movies = []
    movie_containers = soup.find_all('div', class_='box-in')
    for container in movie_containers:
        title = container.find('a')['title']
        trending_movies.append(title)

    return trending_movies
    
@Client.on_message(filters.command("trending"))
def trending_movies(client, message):
    trending_list = get_trending_movies()
    message_text = "Trending Movies:\n\n" + "\n".join(trending_list)
    main = await message.reply_text(message_text)
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=message_text"
        )
        await asyncio.sleep(15)
        await main.delete()

@Client.on_message(filters.command("cinelatest"))
async def cine_latest_movies(client, message):
    msg = await message.reply_text("Fetching latest movies...", quote=True)
    url = f"https://1cinevood.site/"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extracting only the relevant movie information
        movies = soup.find_all('h2', {'class': 'title front-view-title'})
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
        
