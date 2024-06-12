from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS

@Client.on_message(filters.command("add_ott") & filters.user(ADMINS))
async def add_ott(client, message):
    try:
        ott_name = message.text.split(maxsplit=1)[1]
    except IndexError:
        await message.reply("/add_ott Amazon Prime Video")
        return

    try:
        if not await db.is_ott_exist(ott_name):
            await db.add_ott(ott_name)
            await message.reply(f"OTT '{ott_name}' added successfully!")
        else:
            await message.reply(f"OTT '{ott_name}' already adedd!")
    except Exception as e:
        await message.reply(f"An error occurred while adding the OTT platform: {str(e)}")

@Client.on_message(filters.command("ott_list") & filters.user(ADMINS))
async def ott_list_command(client, message):
    ott_list = await db.get_all_otts()
    ott_message = "Current OTT List:\n\n"
    ott_buttons = []

    async for ott in ott_list:
        ott_name = ott['ott_name']
        ott_status = ott['status'] if ott['status'] else "None"
        noti_status = ott['status'] if ott['status'] else "None"

        ott_buttons.append([
            InlineKeyboardButton(f"{ott_name}", callback_data=f"ott_status_toggle_{ott_name}"),
            InlineKeyboardButton(f"ott - {ott_status}", callback_data=f"ott_status_toggle_{ott_name}"),
            InlineKeyboardButton(f"noti - {noti_status}", callback_data=f"noti_status_toggle_{ott_name}")
        ])

    ott_keyboard = InlineKeyboardMarkup(ott_buttons)
    await message.reply(ott_message, reply_markup=ott_keyboard)

@Client.on_callback_query(filters.regex(r"ott_status_toggle_(.+)"))
async def ott_status_toggle_callback(client, callback_query):
    ott_name = callback_query.data.split("_")[2]
    await toggle_ott_status(ott_name)

@Client.on_callback_query(filters.regex(r"noti_status_toggle_(.+)"))
async def noti_status_toggle_callback(client, callback_query):
    ott_name = callback_query.data.split("_")[2]
    await toggle_noti_status(ott_name)

async def toggle_ott_status(ott_name):
    ott = await db.get_ott(ott_name)
    current_status = ott['status'] if ott['status'] else None

    if current_status == "Active":
        new_status = "Down"
    elif current_status == "Down":
        new_status = "Some Video Working"
    else:
        new_status = "Active"

    await db.update_ott(ott_name, True, new_status)
    
async def toggle_noti_status(ott_name):
    ott = await db.get_ott(ott_name)
    current_status = ott['status'] if ott['status'] else None

    if current_status == "Active":
        new_status = "Down"
    elif current_status == "Down":
        new_status = "Some Video Working"
    else:
        new_status = "Active"

    await db.update_ott(ott_name, True, new_status)
