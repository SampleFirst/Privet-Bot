from pyrogram import Client, filters
from database.users_chats_db import db
from info import ADMINS

@Client.on_message(filters.command("add_ott") & filters.user(ADMINS))
async def add_ott(client, message):
    ott_name = message.text.split(maxsplit=1)[1]
    await db.add_ott(ott_name)
    await message.reply(f"OTT '{ott_name}' added successfully!")
