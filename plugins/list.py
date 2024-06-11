from pyrogram import Client, filters
from database.users_chats_db import db
from info import ADMINS


# Command to add an OTT service with status and coins
@Client.on_message(filters.command("add_ott") & filters.user(ADMINS))
async def add_ott_list(client, message):
    # Split the message text into ottname, status, and coins
    _, ottname, status, coins = message.text.split()[1:]
    await db.add_ott(ottname, status, int(coins))
    await message.reply(f"{ottname} added to the OTT list with status: {status} and coins: {coins}")

# Command to get the list of OTT services
@Client.on_message(filters.command("get_ott") & filters.user(ADMINS))
async def get_ott_list(client, message):
    ott_list = await db.get_ott_list()
    ott_list_text = "\n".join(ott_list)
    await message.reply(f"List of OTT services:\n{ott_list_text}")

# Command to delete all OTT services
@Client.on_message(filters.command("delete_all_ott") & filters.user(ADMINS))
async def delete_all_ott(client, message):
    await db.delete_all_ott()
    await message.reply("All OTT services deleted")

