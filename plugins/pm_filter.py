# pm_filter.py
import random
import logging
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from info import ADMINS, PICS, UPI_PIC, LOG_CHANNEL
from database.users_chats_db import db

from utils import check_verification, update_verification
from Script import script

from plugins.datetime import get_datetime 
from plugins.expiry_datetime import get_expiry_datetime, get_expiry_name
from plugins.get_name import get_bot_name, get_db_name
from plugins.status_name import get_status_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

USER_SELECTED = {}
user_states = {}


@Client.on_message(filters.photo & filters.private)
async def payment_screenshot_received(client, message):
    user_id = message.from_user.id
    file_id = str(message.photo.file_id)

    # Check if the user has made a selection before sending the screenshot
    if user_id not in user_states or not user_states[user_id]:
        await message.reply_text("Please select Bot or Database before sending the screenshot.")
        return

    selected_type = USER_SELECTED.get(user_id, "")

    if not selected_type:
        await message.reply_text("Invalid selection. Please start the process again.")
        return

    # Update if and elif conditions for selected_type
    if selected_type in {"Movies Bot", "Anime Bot", "Rename Bot", "YouTube Downloader Bot"}:
        await handle_bot_screenshot(client, message, user_id, selected_type, file_id)
    elif selected_type in {"Movies Database", "Anime Database", "Series Database", "Audio Book Database"}:
        await handle_db_screenshot(client, message, user_id, selected_type, file_id)
    else:
        await message.reply_text("Invalid selection. Start the process again.")

async def handle_bot_screenshot(client, message, user_id, selected_type, file_id):

    selected_type = USER_SELECTED.get(user_id, "")
    user_name = message.from_user.username  # Retrieve user_name from message object

    caption_db = f"User ID: {user_id}\n" \
              f"User Name: {user_name}\n" \
              f"Selected DB: {selected_type}\n"

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirmed", callback_data=f"dbpre"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"payment_cancel_db")
        ]]
    )
    await client.send_photo(chat_id=LOG_CHANNEL, photo=file_id, caption=caption_db, reply_markup=keyboard)
    await message.reply_text(f"Hey {user_name}!\n\nYour Payment Screenshot Received. Wait for Confirmation by Admin.\n\nSending Confirmation Message Soon...")
    user_states[user_id] = False


async def handle_db_screenshot(client, message, user_id, selected_type, file_id):

    selected_type = USER_SELECTED.get(user_id, "")
    user_name = message.from_user.username 

    caption_db = f"User ID: {user_id}\n" \
              f"User Name: {user_name}\n" \
              f"Selected DB: {selected_type}\n"

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirmed", callback_data=f"dbpre"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"payment_cancel_db")
        ]]
    )
    await client.send_photo(chat_id=LOG_CHANNEL, photo=file_id, caption=caption_db, reply_markup=keyboard)
    await message.reply_text(f"Hey {user_name}!\n\nYour Payment Screenshot Received. Wait for Confirmation by Admin.\n\nSending Confirmation Message Soon...")
    user_states[user_id] = False


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()

    elif query.data == "start":
        buttons = [
            [
                InlineKeyboardButton('My Plan', callback_data="plan"),
                InlineKeyboardButton('Status', callback_data="status")
            ],
            [
                InlineKeyboardButton('Bots Premium', callback_data="bots"),
                InlineKeyboardButton('Database Premium', callback_data="database")
            ],
            [
                InlineKeyboardButton('Bots Pack', callback_data="botspack"),
                InlineKeyboardButton('Database Pack', callback_data="dbpack")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("Processing...")
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.START_TXT.format(user=query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "plan":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )

    elif query.data == "status":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )

    elif query.data == "bots":
        buttons = [
            [
                InlineKeyboardButton('Movies Bot', callback_data='mbot'),
                InlineKeyboardButton('Anime Bot', callback_data='abot')
            ],
            [
                InlineKeyboardButton('Rename Bot', callback_data='rbot'),
                InlineKeyboardButton('YT Downloader', callback_data='dbot')
            ],
            [
                InlineKeyboardButton('Back', callback_data='start')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("Processing...")
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.BOTS.format(user=query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "database":
        buttons = [
            [
                InlineKeyboardButton('Movies Database', callback_data='mdb'),
                InlineKeyboardButton('Anime Database', callback_data='adb')
            ],
            [
                InlineKeyboardButton('Series Database', callback_data='sdb'),
                InlineKeyboardButton('Audio Books', callback_data='bdb')
            ],
            [
                InlineKeyboardButton('Back', callback_data='start')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text("Processing...")
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.DATABASE.format(user=query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "botspack":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )

    elif query.data == "dbpack":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )
        
    elif query.data == "mbot" or query.data == "abot" or query.data == "rbot" or query.data == "dbot":
        user_id = query.from_user.id
        user_name = query.from_user.username
        bot_name = get_bot_name(query.data)
        now_status = get_status_name(status_num=1)
        
        now_date = get_datetime(format_type=2)
        now_time = get_datetime(format_type=5)
        expiry_date = get_expiry_datetime(format_type=2, expiry_option="now_to_2m")
        expiry_time = get_expiry_datetime(format_type=5, expiry_option="now_to_2m")
        
        exp_date = get_expiry_datetime(format_type=2, expiry_option="today_to_30d")
        exp_time = get_expiry_datetime(format_type=5, expiry_option="today_to_30d")
        validity = get_expiry_name(expiry_option="today_to_30d")

        if await check_verification(client, user_id, bot_name, now_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {bot_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {bot_name} with {now_status}")
            return 
        else:
            await client.send_message(LOG_CHANNEL, script.LOG_BOT.format(a=user_id, b=user_name, c=bot_name, d=now_status, e=now_date, f=now_time, g=expiry_date, h=expiry_time))
            await update_verification(client, user_id, bot_name, now_status)
            logger.info(f"{user_name} update status for {bot_name} with {now_status}")
            USER_SELECTED[user_id] = bot_name
            buttons = [
                [
                    InlineKeyboardButton('Description', callback_data='botdis'),
                ],
                [
                    InlineKeyboardButton('Buy Premium', callback_data='botbuy'),
                ],
                [
                    InlineKeyboardButton('Go Back', callback_data='bots')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
    
            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS))
            )
            await query.message.edit_text(
                text=script.SELECT_BOT.format(a=bot_name, b=exp_date, c=exp_time, d=validity),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            user_states[user_id] = True

    elif query.data == "mdb" or query.data == "adb" or query.data == "sdb" or query.data == "bdb":
        user_id = query.from_user.id
        user_name = query.from_user.username
        db_name = get_db_name(query.data)
        now_status = get_status_name(status_num=1)
        
        now_date = get_datetime(format_type=2)
        now_time = get_datetime(format_type=5)
        expiry_date = get_expiry_datetime(format_type=2, expiry_option="now_to_2m")
        expiry_time = get_expiry_datetime(format_type=5, expiry_option="now_to_2m")
        
        exp_date = get_expiry_datetime(format_type=2, expiry_option="today_to_30d")
        exp_time = get_expiry_datetime(format_type=5, expiry_option="today_to_30d")
        validity = get_expiry_name(expiry_option="today_to_30d")

        if await check_verification(client, user_id, db_name, now_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {db_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {db_name} with {now_status}")
            return 
        else:
            await client.send_message(LOG_CHANNEL, script.LOG_DB.format(a=user_id, b=user_name, c=db_name, d=now_status, e=now_date, f=now_time, g=expiry_date, h=expiry_time))
            await update_verification(client, user_id, db_name, now_status)
            logger.info(f"{user_name} update status for {db_name} with {now_status}")
            USER_SELECTED[user_id] = db_name
            buttons = [
                [
                    InlineKeyboardButton('Description', callback_data='dbdis'),
                ],
                [
                    InlineKeyboardButton('Buy Premium', callback_data='dbbuy'),
                ],
                [
                    InlineKeyboardButton('Go Back', callback_data='bots')
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)

            await client.edit_message_media(
                query.message.chat.id,
                query.message.id,
                InputMediaPhoto(random.choice(PICS))
            )
            await query.message.edit_text(
                text=script.SELECT_DB.format(a=db_name, b=exp_date, c=exp_time, d=validity),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            user_states[user_id] = True
            
    elif query.data == "botbuy":
        user_id = query.from_user.id  # Assigning user_id here
        selected_type = USER_SELECTED.get(user_id, "")
        buttons = [
            [
                InlineKeyboardButton('Go Back', callback_data='bots')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(UPI_PIC)
        )
        await query.message.edit_text(
            text=script.BUY_BOT.format(bot_name=selected_type),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "dbbuy":
        user_id = query.from_user.id  # Assigning user_id here
        selected_type = USER_SELECTED.get(user_id, "")
        buttons = [
            [
                InlineKeyboardButton('Go Back', callback_data='bots')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(UPI_PIC)
        )
        await query.message.edit_text(
            text=script.BUY_DB.format(db_name=selected_type),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "botpre":
        await query.message.edit_text(
            text=script.BUY_BOT_PREMIUM.format(db_name=db_name),
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "dbpre":
        await query.message.edit_text(
            text=script.BUY_DB_PREMIUM.format(user=query.from_user.mention),
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "botdis":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )

    elif query.data == "dbdis":
        await query.answer(
            text=script.CONSTRUCTION.format(user=query.from_user.mention),
            show_alert=True
        )
        
