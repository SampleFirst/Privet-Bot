# pm_filter.py
import random
import logging
import asyncio

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto

from info import ADMINS, PICS, LOG_CHANNEL
from database.users_chats_db import db

from utils import check_verification, update_verification
from Script import script

from plugins.datetime import get_datetime 
from plugins.expiry_datetime import get_expiry_datetime, get_expiry_name
from plugins.get_name import get_bot_name, get_db_name
from plugins.status_name import get_status_name

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data
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

    elif data == "bots":
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

    elif data == "database":
        buttons = [
            [
                InlineKeyboardButton('Movies Database', callback_data='mdb'),
                InlineKeyboardButton('Anime Database', callback_data='adb')
            ],
            [
                InlineKeyboardButton('TV Show Database', callback_data='sdb'),
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
        
        if await check_verification(client, user_id, bot_name, now_status):
            await query.answer(f"Hey {user_name}! Sorry, but you already have an active request for {bot_name}.", show_alert=True)
            logger.info(f"{user_name} has Active status for {bot_name} with {now_status}")
            return 
        else:
            await client.send_message(LOG_CHANNEL, script.LOG_BOT.format(a=user_id, b=user_name, c=bot_name, d=now_status, e=now_date, f=now_time, g=expiry_date, h=expiry_time)
            await update_verification(client, user_id, bot_name, now_status)
            logger.info(f"{user_name} update status for {bot_name} with {now_status}")
            buttons = [
                [
                    InlineKeyboardButton('Description', callback_data='botdis'),
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
                text=script.SELECT_BOT.format(user=query.from_user.mention, bot_name=bot_name),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )

    elif data == "botpre":
        await query.message.edit_text(
            text=script.BUY_BOT_PREMIUM.format(user=query.from_user.mention),
            parse_mode=enums.ParseMode.HTML
        )

    elif data == "dbpre":
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
        
