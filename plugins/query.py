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

REVERSE_STATUS_MAPPING = {v: k for k, v in STATUS_MAPPING.items()}

async def toggle_ott_status(ott_name):
    ott = await db.get_ott(ott_name)
    current_status_num = STATUS_MAPPING.get(ott['ott_status']['status'], 4) if 'ott_status' in ott else 4
    new_status_num = (current_status_num % 4) + 1
    new_status = REVERSE_STATUS_MAPPING[new_status_num]
    await db.update_ott(ott_name, 'ott_status', new_status)


async def toggle_noti_status(ott_name):
    ott = await db.get_ott(ott_name)
    current_status_num = STATUS_MAPPING.get(ott['noti_status']['status'], 4) if 'noti_status' in ott else 4
    new_status_num = (current_status_num % 4) + 1
    new_status = REVERSE_STATUS_MAPPING[new_status_num]
    await db.update_ott(ott_name, 'noti_status', new_status)

@Client.on_callback_query(filters.regex('toggle_'))
async def toggle_settings(client, callback_query):
    setting = callback_query.data.split('_')[1]
    settings = await db.get_settings()
    if setting == "refer":
        settings['refer_on'] = not settings.get('refer_on', False)
    elif setting == "bonus":
        settings['daily_bonus'] = not settings.get('daily_bonus', False)
    elif setting == "withdraw":
        settings['withdraw_btn'] = not settings.get('withdraw_btn', False)
        
    await db.update_settings(settings)
    
    buttons = [
        [
            InlineKeyboardButton('Refer Earn', callback_data="refer"),
            InlineKeyboardButton('✅ ON' if settings["refer_on"] else '❌ OFF', callback_data="toggle_refer")
        ],
        [
            InlineKeyboardButton('Daily Bonus', callback_data="bonus"),
            InlineKeyboardButton('✅ ON' if settings["daily_bonus"] else '❌ OFF', callback_data="toggle_bonus")
        ],
        [
            InlineKeyboardButton('Withdraw BTN', callback_data="withdraw"),
            InlineKeyboardButton('✅ Always ON' if settings["withdraw_btn"] else '❌ After Earn', callback_data="toggle_withdraw")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_reply_markup(reply_markup=reply_markup)


@Client.on_callback_query(filters.regex(r"ott_status_toggle_(.+)"))
async def ott_status_toggle_callback(client, callback_query):
    ott_name = callback_query.data.split("_")[2]
    await toggle_ott_status(ott_name)
    await callback_query.answer("OTT status updated")


@Client.on_callback_query(filters.regex(r"noti_status_toggle_(.+)"))
async def noti_status_toggle_callback(client, callback_query):
    ott_name = callback_query.data.split("_")[2]
    await toggle_noti_status(ott_name)
    await callback_query.answer("Notification status updated")


