from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.users_chats_db import db
from info import ADMINS

STATUS_MAPPING = {
    "Active": 1,
    "Down": 2,
    "Some Video Working": 3,
    "None": 4
}

REVERSE_STATUS_MAPPING = {v: k for k, v in STATUS_MAPPING.items()}


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    
    elif query.data.startswith('toggle_'):
        setting = query.data.split('_')[1]
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
        await query.message.edit_reply_markup(reply_markup=reply_markup)

    elif query.data.startswith('ott_status_toggle_'):
        ott_name = query.data.split("_")[2]
        ott = await db.get_ott(ott_name)
        current_status_num = STATUS_MAPPING.get(ott['ott_status']['status'], 4) if 'ott_status' in ott else 4
        new_status_num = (current_status_num % 4) + 1
        new_status = REVERSE_STATUS_MAPPING[new_status_num]
        await db.update_ott(ott_name, 'ott_status', new_status)
        await query.answer("OTT status updated")

        ott_list = await db.get_all_otts()
        ott_message = "Current OTT List:\n\n1 = Active\n2 = Down\n3 = Some Video Working\n4 = None"
        ott_buttons = []
    
        async for ott in ott_list:
            ott_name = ott['ott_name']
            ott_status = STATUS_MAPPING.get(ott['ott_status']['status'], 4) if 'ott_status' in ott else 4
            noti_status = STATUS_MAPPING.get(ott['noti_status']['status'], 4) if 'noti_status' in ott else 4
    
            ott_buttons.append([
                InlineKeyboardButton(f"{ott_name}", callback_data=f"ott_status_toggle_{ott_name}"),
                InlineKeyboardButton(f"ott - {ott_status}", callback_data=f"ott_status_toggle_{ott_name}"),
                InlineKeyboardButton(f"noti - {noti_status}", callback_data=f"noti_status_toggle_{ott_name}")
            ])
    
        ott_keyboard = InlineKeyboardMarkup(ott_buttons)
        await message.reply(ott_message, reply_markup=ott_keyboard)

    elif query.data.startswith('noti_status_toggle_'):
        ott_name = query.data.split("_")[2]
        ott = await db.get_ott(ott_name)
        current_status_num = STATUS_MAPPING.get(ott['noti_status']['status'], 4) if 'noti_status' in ott else 4
        new_status_num = (current_status_num % 4) + 1
        new_status = REVERSE_STATUS_MAPPING[new_status_num]
        await db.update_ott(ott_name, 'noti_status', new_status)
        await query.answer("Notification status updated")
        
