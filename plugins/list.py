from pyrogram import Client, filters
from database.users_chats_db import db
from info import ADMINS

# Command to add an OTT service with status and coins
@Client.on_message(filters.command("add_ott") & filters.user(ADMINS))
async def add_ott(client, message):
    usage = "Usage: /add_ott 'ottname' 'status: Active/Down/Some Videos Working' 'coins'"
    try:
        command, ottname, status, coins = message.text.split("'")[1::2]
        if status.lower() not in ["Active", "Down", "Some Videos Working"]:
            await message.reply("Invalid status! Status must be one of: Active, Down, Some Videos Working.")
            return
        await db.add_ott(ottname, status, int(coins))
        await message.reply(f"{ottname} added to the OTT list with status: {status} and coins: {coins}")
    except ValueError:
        await message.reply(usage)
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Command to get the list of OTT services
@Client.on_message(filters.command("ott_list") & filters.user(ADMINS))
async def ott_list(client, message):
    ott_list = await db.get_ott_list()
    if ott_list:
        ott_list_text = "\n".join(ott_list)
        await message.reply(f"List of OTT services:\n{ott_list_text}")
    else:
        await message.reply("No OTT services found.")

# Command to delete all OTT services
@Client.on_message(filters.command("delete_all_ott") & filters.user(ADMINS))
async def delete_all_ott(client, message):
    await db.delete_all_ott()
    await message.reply("All OTT services deleted")

