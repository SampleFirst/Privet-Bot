from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS

STATUS_MAPPING = {
    "Active": 1,
    "Down": 2,
    "Some Video Working": 3,
    "None": 4
}


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
async def ott_list(client, message):
    ott_list = await db.get_all_otts()
    ott_message = "Current OTT List:\n\n1 = Active\n2 = Down\n3 = Some Video Working\n4 = None"
    ott_buttons = []

    async for ott in ott_list:
        ott_name = ott['ott_name']
        ott_status = STATUS_MAPPING.get(ott['ott_status']['status'], 4) if 'ott_status' in ott else 4
        noti_status = STATUS_MAPPING.get(ott['noti_status']['status'], 4) if 'noti_status' in ott else 4

        ott_buttons.append([
            InlineKeyboardButton(f"{ott_name}", callback_data=f"ott_status_toggle_{ott_name}_{ott_status}"),
            InlineKeyboardButton(f"ott - {ott_status}", callback_data=f"ott_status_toggle_{ott_name}_{ott_status}"),
            InlineKeyboardButton(f"noti - {noti_status}", callback_data=f"noti_status_toggle_{ott_name}_{noti_status}")
        ])

    ott_keyboard = InlineKeyboardMarkup(ott_buttons)
    await message.reply(ott_message, reply_markup=ott_keyboard)


@Client.on_message(filters.command("delete_all_ott") & filters.user(ADMINS))
async def delete_all_ott(client, message):
    await db.delete_all_ott()
    await message.reply("All OTT services deleted")

