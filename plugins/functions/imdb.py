import os
from pyrogram import Client, filters, enums
from info import IMDB_TEMPLATE
from utils import get_poster
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

invite_url = ""

# Define a command handler to store the invite URL
@Client.on_message(filters.command("store_url") & filters.private)
def store_invite_url(client, message):
    global invite_url
    
    command_parts = message.text.split("/store_url ", 1)
    text = command_parts[1]
    
    # Check if the text contains a Telegram invite URL
    if "https://t.me/" in text:
        invite_url = text
        message.reply_text(f"Invite URL stored: {invite_url}")
    else:
        message.reply_text("No valid Telegram invite URL found in the message.")

# Define a command handler to get the stored invite URL
@Client.on_message(filters.command("get_url") & filters.private)
def get_invite_url(client, message):
    global invite_url
    
    if invite_url:
        message.reply_text(f"Stored Invite URL: {invite_url}")
    else:
        message.reply_text("No URL has been stored yet.")


@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching ImDB')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, quer_y: CallbackQuery):
    global invite_url
    i, movie = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    
    if invite_url:
        btn = [
                [
                    InlineKeyboardButton(
                        text=f"Direct File - {imdb.get('title')}",
                        url=invite_url,
                    )
                ]
            ]
        message = quer_y.message.reply_to_message or quer_y.message
        if imdb:
            caption = IMDB_TEMPLATE.format(
                query = imdb['title'],
                title = imdb['title'],
                votes = imdb['votes'],
                aka = imdb["aka"],
                seasons = imdb["seasons"],
                box_office = imdb['box_office'],
                localized_title = imdb['localized_title'],
                kind = imdb['kind'],
                imdb_id = imdb["imdb_id"],
                cast = imdb["cast"],
                runtime = imdb["runtime"],
                countries = imdb["countries"],
                certificates = imdb["certificates"],
                languages = imdb["languages"],
                director = imdb["director"],
                writer = imdb["writer"],
                producer = imdb["producer"],
                composer = imdb["composer"],
                cinematographer = imdb["cinematographer"],
                music_team = imdb["music_team"],
                distributors = imdb["distributors"],
                release_date = imdb['release_date'],
                year = imdb['year'],
                genres = imdb['genres'],
                poster = imdb['poster'],
                plot = imdb['plot'],
                rating = imdb['rating'],
                url = imdb['url'],
                **locals()
            )
        else:
            caption = "No Results"
        if imdb.get('poster'):
            try:
                await quer_y.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                pic = imdb.get('poster')
                poster = pic.replace('.jpg', "._V1_UX360.jpg")
                await quer_y.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
            except Exception as e:
                logger.exception(e)
                await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
            await quer_y.message.delete()
        else:
            await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.answer()
    else:
        message.reply_text("No URL has been stored yet.")

