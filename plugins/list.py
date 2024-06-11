from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.users_chats_db import db
from info import ADMINS

status_options = ["Active", "Down", "Some Videos Working", "None"]

@Client.on_message(filters.command("add_ott") & filters.user(ADMINS))
async def add_ott(client, message):
    try:
        command_parts = message.text.split()
        ottname = " ".join(command_parts[1:-1])
        coins = int(command_parts[-1])
    except (IndexError, ValueError):
        await message.reply("Usage: /add_ott ottname coins")
        return

    buttons = [
        [InlineKeyboardButton(option, callback_data=f"add_ott:{ottname}:{coins}:{option}")]
        for option in status_options
    ]
    reply_markup = InlineKeyboardMarkup(buttons)

    await message.reply(f"OTT Name: {ottname}\nCoins: {coins}\nSelect Status:", reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r"add_ott:(.*):(.*):(.*)"))
async def add_ott_callback(client, callback_query: CallbackQuery):
    _, ottname, coins, status = callback_query.data.split(":")
    await db.add_ott(ottname, status, int(coins))
    await callback_query.message.edit_text(f"Added OTT Service:\nName: {ottname}\nCoins: {coins}\nStatus: {status}")
    await callback_query.answer("OTT service added successfully.")


# Command to get the list of OTT services
@Client.on_message(filters.command("ott_list") & filters.user(ADMINS))
async def ott_list(client, message):
    user = message.from_user.mention
    ott_list = await db.get_ott_list()
    if ott_list:
        response = "Hi {user}! I am one and only DRM Downloader Bot on [Telegram](https://telegram.org/):\n\nAwailable OTTs:"
        async for index, ott in enumerate(ott_list, start=1):
            response += f"{index}) {ott['ottname']} ({ott['status']}){'_' * (30 - len(ott['ottname']) - len(ott['status']) - len(str(index)) - 3)}{ott['credits']} Credits\n"
        await message.reply(response)
    else:
        await message.reply("No OTT services found.")

# Command to delete all OTT services
@Client.on_message(filters.command("delete_all_ott") & filters.user(ADMINS))
async def delete_all_ott(client, message):
    await db.delete_all_ott()
    await message.reply("All OTT services deleted")

