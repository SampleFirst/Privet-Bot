# gethtml.py
import os
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from info import ADMINS, LOG_CHANNEL
import tldextract

logging.basicConfig(level=logging.ERROR)



@Client.on_message(filters.command("gethtml") & filters.user(ADMINS))
async def get_html(client, message):
    try:
        if len(message.command) != 2:
            await message.reply_text("Please provide a URL.")
            return        
        usr_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/61.0.3163.100 Safari/537.36'
        }
        url = message.text.split()[1]
        msg = await message.reply_text(f"Fetching HTML code for {url}...")
        response = requests.get(url, headers=usr_agent)
        response.raise_for_status()
        html = response.text
        ext = tldextract.extract(url)
        domain = ext.domain
        suffix = ext.suffix
        file_path = f"{domain}.{suffix}.html"
        caption = f"HTML code sent successfully!\n\nDomain Name: {domain}\nSuffix: {suffix}\n\nWebsite: {url}"
        with open(file_path, "w") as f:
            f.write(html)
        await msg.delete()        
        await message.reply_document(
            document=file_path,
            caption=caption
        )
        await client.send_document(
            chat_id=LOG_CHANNEL,
            document=file_path,
            caption=caption
        )
        os.remove(file_path)
    except Exception as e:
        await message.reply_text(f"Error fetching HTML code: {e}")
