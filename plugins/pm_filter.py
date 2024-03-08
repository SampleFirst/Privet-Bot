# pm_filter.py
import random
import logging
import asyncio
import pytz

from datetime import date, time, datetime, timedelta
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from info import ADMINS, PICS, UPI_PIC, LOG_CHANNEL, PREMIUM_LOGS, PAYMENT_CHAT, MOVIES_DB, ANIME_DB, SERIES_DB, AUDIOBOOK_DB
from database.users_chats_db import db

from utils import send_invite_link, check_verification, update_verification
from Script import script

from plugins.datetime import get_datetime 
from plugins.expiry_datetime import get_expiry_datetime, get_expiry_name
from plugins.get_name import get_bot_name, get_db_name
from plugins.status_name import get_status_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

USER_SELECTED = {}
USER_STATES = {}



@Client.on_message(filters.photo & filters.private)
async def payment_screenshot_received(client, message):
    user_id = message.from_user.id
    file_id = str(message.photo.file_id)
    
    if user_id not in USER_STATES or not USER_STATES[user_id]:
        await message.reply_text("Please select Bot or Database before sending the screenshot.")
        return

    selected_bot = USER_SELECTED.get(user_id, "")

    if not selected_bot:
        await message.reply_text("Invalid selection. Please start the process again.")
        return

    if selected_bot in {"Movies Bot", "File to Link Bot", "Rename Bot", "YouTube Downloader Bot"}:
        await handle_bot_screenshot(client, message, user_id, selected_bot, file_id)
    elif selected_bot in {"Movies Database", "Anime Database", "Series Database", "Audio Book Database"}:
        await handle_db_screenshot(client, message, user_id, selected_bot, file_id)
    else:
        await message.reply_text("Invalid selection. Start the process again.")


async def handle_bot_screenshot(client, message, user_id, selected_bot, file_id):
    user_name = message.from_user.username  # Retrieve user_name from message object
    now_dt = get_datetime(format_type=23)
    exp_dt = get_expiry_datetime(format_type=23, expiry_option="today_to_30d")
    now_status = get_status_name(status_num=2)

    caption_db = (
        f"User ID: {user_id}\n"
        f"User Name: {user_name}\n"
        f"Bot Name: {selected_bot}\n"
        f"Now Datetime: {now_dt}\n"
        f"Exp Datetime: {exp_dt}\n"
    )

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirmed", callback_data="botpre")
        ],[
            InlineKeyboardButton("❌ Invalid Payment", callback_data="botcan1"),
            InlineKeyboardButton("❌ Short Payment", callback_data="botcan2"),
        ]]
    )
    await client.send_photo(chat_id=LOG_CHANNEL, photo=file_id, caption=caption_db, reply_markup=keyboard)
    await update_verification(client, user_id, selected_bot, now_status)
    logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
    await message.reply_text(f"Hey {user_name}!\n\nYour Payment Screenshot Received. Wait for Confirmation by Admin.\n\nSending Confirmation Message Soon...")
    USER_STATES[user_id] = False 

async def handle_db_screenshot(client, message, user_id, selected_bot, file_id):
    user_name = message.from_user.username  # Retrieve user_name from message object
    now_dt = get_datetime(format_type=23)
    exp_dt = get_expiry_datetime(format_type=23, expiry_option="today_to_30d")
    now_status = get_status_name(status_num=2)

    caption_db = (
        f"User ID: {user_id}\n"
        f"User Name: {user_name}\n"
        f"Database: {selected_bot}\n"
        f"Now Datetime: {now_dt}\n"
        f"Exp Datetime: {exp_dt}\n"
    )

    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("✅ Confirmed", callback_data="dbpre")
        ],[
            InlineKeyboardButton("❌ Invalid Payment", callback_data="dbcan1"),
            InlineKeyboardButton("❌ Short Payment", callback_data="dbcan2"),
        ]]
    )
    await client.send_photo(chat_id=LOG_CHANNEL, photo=file_id, caption=caption_db, reply_markup=keyboard)
    await update_verification(client, user_id, selected_bot, now_status)
    logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
    await message.reply_text(f"Hey {user_name}!\n\nYour Payment Screenshot Received. Wait for Confirmation by Admin.\n\nSending Confirmation Message Soon...")
    USER_STATES[user_id] = False 

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    is_admin = query.from_user.id in ADMINS
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
                InlineKeyboardButton('File to Link Bot', callback_data='fbot')
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
        
    elif query.data == "mbot" or query.data == "fbot" or query.data == "rbot" or query.data == "dbot":
        user_id = query.from_user.id
        user_name = query.from_user.username
        bot_name = get_bot_name(query.data)
        
        now_date = get_datetime(format_type=2)
        now_time = get_datetime(format_type=5)
        expiry_date = get_expiry_datetime(format_type=2, expiry_option="now_to_2m")
        expiry_time = get_expiry_datetime(format_type=5, expiry_option="now_to_2m")
        
        exp_date = get_expiry_datetime(format_type=2, expiry_option="today_to_30d")
        exp_time = get_expiry_datetime(format_type=5, expiry_option="today_to_30d")
        validity = get_expiry_name(expiry_option="today_to_30d")

        premium_status = get_status_name(status_num=3)
        confirm_status = get_status_name(status_num=2)
        attempt_status = get_status_name(status_num=1)
        
        if await check_verification(client, user_id, bot_name, premium_status):
            await query.answer(f"Hey {user_name}! you already have an Premium for {bot_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {bot_name} with {premium_status}")
            return
        elif await check_verification(client, user_id, bot_name, confirm_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {bot_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {bot_name} with {confirm_status}")
            return
        elif await check_verification(client, user_id, bot_name, attempt_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {bot_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {bot_name} with {attempt_status}")
            return
        else:
            await client.send_message(LOG_CHANNEL, script.LOG_BOT.format(a=user_id, b=user_name, c=bot_name, d=attempt_status, e=now_date, f=now_time, g=expiry_date, h=expiry_time))
            await update_verification(client, user_id, bot_name, attempt_status)
            logger.info(f"{user_name} update status for {bot_name} with {attempt_status}")
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
            USER_STATES[user_id] = True

    elif query.data == "mdb" or query.data == "adb" or query.data == "sdb" or query.data == "bdb":
        user_id = query.from_user.id
        user_name = query.from_user.username
        db_name = get_db_name(query.data)
        
        now_date = get_datetime(format_type=2)
        now_time = get_datetime(format_type=5)
        expiry_date = get_expiry_datetime(format_type=2, expiry_option="now_to_2m")
        expiry_time = get_expiry_datetime(format_type=5, expiry_option="now_to_2m")
        
        exp_date = get_expiry_datetime(format_type=2, expiry_option="today_to_30d")
        exp_time = get_expiry_datetime(format_type=5, expiry_option="today_to_30d")
        validity = get_expiry_name(expiry_option="today_to_30d")

        premium_status = get_status_name(status_num=3)
        confirm_status = get_status_name(status_num=2)
        attempt_status = get_status_name(status_num=1)
        
        if await check_verification(client, user_id, db_name, premium_status):
            await query.answer(f"Hey {user_name}! you already have an Premium for {db_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {db_name} with {premium_status}")
            return
        elif await check_verification(client, user_id, db_name, confirm_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {db_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {db_name} with {confirm_status}")
            return
        elif await check_verification(client, user_id, db_name, attempt_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {db_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {db_name} with {attempt_status}")
            return
        else:
            await client.send_message(LOG_CHANNEL, script.LOG_DB.format(a=user_id, b=user_name, c=db_name, d=attempt_status, e=now_date, f=now_time, g=expiry_date, h=expiry_time))
            await update_verification(client, user_id, db_name, attempt_status)
            logger.info(f"{user_name} update status for {db_name} with {attempt_status}")
            USER_SELECTED[user_id] = db_name
            buttons = [
                [
                    InlineKeyboardButton('Description', callback_data='dbdis'),
                ],
                [
                    InlineKeyboardButton('Buy Premium', callback_data='dbbuy'),
                ],
                [
                    InlineKeyboardButton('Go Back', callback_data='database')
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
            USER_STATES[user_id] = True
            
    elif query.data == "botbuy":
        user_id = query.from_user.id
        user_name = query.from_user.username
        bot_name = USER_SELECTED.get(user_id, "")
        now_status = get_status_name(status_num=2)
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
            text=script.BUY_BOT.format(bot_name=bot_name),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "dbbuy":
        user_id = query.from_user.id
        user_name = query.from_user.username
        db_name = USER_SELECTED.get(user_id, "")
        now_status = get_status_name(status_num=2)
        buttons = [
            [
                InlineKeyboardButton('Go Back', callback_data='database')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(UPI_PIC)
        )
        await query.message.edit_text(
            text=script.BUY_DB.format(db_name=db_name),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    
    elif query.data == "botpre":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_bot = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=3)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="today_to_30d")
            
            if selected_bot == 'Movies Bot':
                await client.send_message(PAYMENT_CHAT, f"/add {user_id}")
            elif selected_bot == 'File to Link Bot':
                await client.send_message(PAYMENT_CHAT, f"/pre {user_id}")
            elif selected_bot == 'Rename Bot':
                await client.send_message(PAYMENT_CHAT, f"/try {user_id}")
            elif selected_bot == 'YouTube Downloader Bot':
                await client.send_message(PAYMENT_CHAT, f"/pro {user_id}")
                
            await update_verification(client, user_id, selected_bot, now_status)
            logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
            await client.send_message(user_id, "Done! 🎉 Congratulations, you've upgraded to Premium for {selected_bot}! 🌟 Check out your plan details in /myplan...", parse_mode=enums.ParseMode.HTML)
            await client.send_message(
                PREMIUM_LOGS,
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "dbpre":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_db = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=3)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="today_to_30d")
        
            await send_invite_link(client, user_id, selected_db)
            await update_verification(client, user_id, selected_db, now_status)
            logger.info(f"{user_name} update status for {selected_db} with {now_status}")
    
            await client.send_message(
                PREMIUM_LOGS,
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "botcan1":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_bot = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=6)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="now_to_2m")
            
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("✅ Confirmed", callback_data="botpre")
                ],[
                    InlineKeyboardButton("❌ Invalid Payment", callback_data="botcan1"),
                    InlineKeyboardButton("❌ Short Payment", callback_data="botcan2"),
                ]]
            )
            await update_verification(client, user_id, selected_bot, now_status)
            logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
            await client.send_message(user_id, f"Cancel! ❌ Attention, Sorry for cancelling the upgrade process due to an invalid payment screenshot! 📵 Please send a valid screenshot. If you have any questions, contact the admin in /send.", parse_mode=enums.ParseMode.HTML)
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "botcan2":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_bot = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=6)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="now_to_2m")
            
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("✅ Confirmed", callback_data="botpre")
                ],[
                    InlineKeyboardButton("❌ Invalid Payment", callback_data="botcan1"),
                    InlineKeyboardButton("❌ Short Payment", callback_data="botcan2"),
                ]]
            )
            await update_verification(client, user_id, selected_bot, now_status)
            logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
            await client.send_message(user_id, f"Cancel! ❌ Attention, Sorry for cancelling the upgrade process as full payment wasn't made at once! 💳 If you have any questions, contact the admin in /send.", parse_mode=enums.ParseMode.HTML)
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "dbcan1":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_bot = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=6)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="now_to_2m")
            
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("✅ Confirmed", callback_data="dbpre")
                ],[
                    InlineKeyboardButton("❌ Invalid Payment", callback_data="dbcan1"),
                    InlineKeyboardButton("❌ Short Payment", callback_data="dbcan2"),
                ]]
            )
            await update_verification(client, user_id, selected_bot, now_status)
            logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
            await client.send_message(user_id, f"Cancel! ❌ Attention, Sorry for cancelling the upgrade process due to an invalid payment screenshot! 📵 Please send a valid screenshot. If you have any questions, contact the admin in /send.", parse_mode=enums.ParseMode.HTML)
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "dbcan2":
        if is_admin:
            user_id = query.from_user.id
            user_name = query.from_user.username
            selected_bot = USER_SELECTED.get(user_id, "")
            now_status = get_status_name(status_num=6)
            now_date = get_datetime(format_type=23)
            expiry_date = get_expiry_datetime(format_type=23, expiry_option="now_to_2m")
            
            keyboard = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("✅ Confirmed", callback_data="dbpre")
                ],[
                    InlineKeyboardButton("❌ Invalid Payment", callback_data="dbcan1"),
                    InlineKeyboardButton("❌ Short Payment", callback_data="dbcan2"),
                ]]
            )
            await update_verification(client, user_id, selected_bot, now_status)
            logger.info(f"{user_name} update status for {selected_bot} with {now_status}")
            await client.send_message(user_id, f"Cancel! ❌ Attention, Sorry for cancelling the upgrade process as full payment wasn't made at once! 💳 If you have any questions, contact the admin in /send.", parse_mode=enums.ParseMode.HTML)
            await query.message.edit_text(
                text=script.LOG_PREDB.format(a=user_id, b=user_name, c=now_status, d=now_date, e=expiry_date),
                reply_markup=keyboard,
                parse_mode=enums.ParseMode.HTML
            )
        else:
            await query.answer('This Button Only For ADMINS', show_alert=True)
    
    elif query.data == "botdis":
        user_id = query.from_user.id
        selected_bot = USER_SELECTED.get(user_id, "")
        description_text = ""
    
        if selected_bot == "Movies Bot'":
            description_text = script.MOVIES_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "File to Link Bot":
            description_text = script.LINK_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "Rename Bot":
            description_text = script.RENAME_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "YouTube Downloader Bot":
            description_text = script.YT_TEXT.format(user=query.from_user.mention)
    
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=description_text,
            parse_mode=enums.ParseMode.MARKDOWN
        )
    
    elif query.data == "dbdis":
        user_id = query.from_user.id
        selected_bot = USER_SELECTED.get(user_id, "")
        description_text = ""
        
        if selected_bot == "Movies Database":
            description_text = script.MOVIESDB_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "Anime Database":
            description_text = script.ANIMEDB_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "Series Database'":
            description_text = script.SERIESDB_TEXT.format(user=query.from_user.mention)
        elif selected_bot == "Audio Book Database":
            description_text = script.BOOKSDB_TEXT.format(user=query.from_user.mention)
        
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=description_text,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        
        
