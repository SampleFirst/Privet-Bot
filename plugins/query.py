import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, REFERRAL_ON
from utils import is_subscribed, temp, get_size, check_verification, get_token, check_token
from Script import script
import time
import datetime
import pytz

logger = logging.getLogger(__name__)



@Client.on_callback_query(filters.regex('toggle_'))
async def toggle_settings(client, callback_query):
    setting = callback_query.data.split('_')[1]
    settings = await db.get_settings()
    if setting == "refer":
        settings['refer'] = not settings.get('refer', False)
    elif setting == "bonus":
        settings['daily_bonus'] = not settings.get('daily_bonus', False)
    
    await db.update_settings(settings)
    
    buttons = [
        [
            InlineKeyboardButton('Refer Earn', callback_data="toggle_refer"),
            InlineKeyboardButton('ON' if settings["refer"] else 'OFF', callback_data="toggle_refer")
        ],
        [
            InlineKeyboardButton('Daily Bonus', callback_data="toggle_bonus"),
            InlineKeyboardButton('✅ Yes' if settings["daily_bonus"] else '❌ No', callback_data="toggle_bonus")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
