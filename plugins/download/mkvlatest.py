import asyncio
import requests
from bs4 import BeautifulSoup
from pyrogram import Client, filters
from info import ADMINS, LOG_CHANNEL


@Client.on_message(filters.command("mkvtrending"))
async def mkv_trending(client, message):
    msg = await message.reply_text("Fetching trending movies...", quote=True)
    url = "https://mkvcinemas.nexus/"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")
        movies = soup.find_all("div", {'class': 'ml-mask jt'})
        movie_list = ""
        for movie in movies:
            movie_list += f"<code>{movie.find('span', {'class': 'mli-info'}).text}</code>\n\n"

        await msg.edit_text(f"Most Popular Movies:\n\n{movie_list}", quote=True)
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"Latest Updated Movies:\n\n{movie_list}"
        )
        await asyncio.sleep(15)
        await msg.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
