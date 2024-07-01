import logging
from typing import Union
import pytz
import random 
import re
import os
import asyncio
import pytz
import time
from Script import script
from datetime import datetime
from pyrogram.errors import FloodWait, UserIsBlocked
from datetime import datetime, timedelta, date, time
import string
from typing import List
from database.users_chats_db import db
import requests
import aiohttp
from info import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

TOKENS = {}
VERIFIED = {}

# temp db for banned 
class temp(object):
    VERIFY = {}
    ME = None
    U_NAME = None
    B_NAME = None
    USERS_CANCEL = False

async def is_subscribed(bot, query=None, userid=None):
    try:
        if userid is None and query is not None:
            user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
        else:
            user = await bot.get_chat_member(AUTH_CHANNEL, int(userid))
    except Exception as e:
        logger.exception(e)
        return False
    else:
        if user.status != "kicked":
            return True
    return False

def extract_commands(file_path):
    commands = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'filters\.command\(["\'](\w+)["\']', line)
            if match:
                commands.append(match.group(1))
    return commands

async def get_user_list(page, sort_by):
    users_cursor = await db.get_all_users()
    users = await users_cursor.to_list(length=None)

    if sort_by == "highest":
        users = sorted(users, key=lambda x: x['coins'], reverse=True)
    elif sort_by == "lowest":
        users = sorted(users, key=lambda x: x['coins'])
    
    start_index = (page - 1) * 10
    end_index = start_index + 10
    total_coins = sum(user['coins'] for user in users)
    return users[start_index:end_index], len(users), total_coins

def get_size(size):
    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

async def broadcast_messages(bot, user_id, message, pin):
    try:
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return await broadcast_messages(bot, user_id, message, pin)
    except UserIsBlocked:
        await bot.unban_chat_member(user_id, bot.id)
        m = await message.copy(chat_id=user_id)
        if pin:
            await m.pin(both_sides=True)
        return "Success"
    except Exception as e:
        return "Error"

def get_readable_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result
    
async def get_verify_shorted_link(num, link):
    if int(num) == 1:
        API = SHORTLINK_API
        URL = SHORTLINK_URL
    elif int(num) == 2:
        API = VERIFY2_API
        URL = VERIFY2_URL
    elif int(num) == 3:
        API = VERIFY3_API
        URL = VERIFY3_URL
    elif int(num) == 4:
        API = VERIFY4_API
        URL = VERIFY4_URL
    elif int(num) == 5:
        API = VERIFY5_API
        URL = VERIFY5_URL
    elif int(num) == 6:
        API = VERIFY6_API
        URL = VERIFY6_URL
    elif int(num) == 7:
        API = VERIFY7_API
        URL = VERIFY7_URL
    elif int(num) == 8:
        API = VERIFY8_API
        URL = VERIFY8_URL
    elif int(num) == 9:
        API = VERIFY9_API
        URL = VERIFY9_URL
    else:
        API = VERIFY10_API
        URL = VERIFY10_URL
    https = link.split(":")[0]
    if "http" == https:
        https = "https"
        link = link.replace("http", https)

    if URL == "api.shareus.in":
        url = f"https://{URL}/shortLink"
        params = {"token": API,
                  "format": "json",
                  "link": link,
                  }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.json(content_type="text/html")
                    if data["status"] == "success":
                        return data["shortlink"]
                    else:
                        logger.error(f"Error: {data['message']}")
                        return f'https://{URL}/shortLink?token={API}&format=json&link={link}'

        except Exception as e:
            logger.error(e)
            return f'https://{URL}/shortLink?token={API}&format=json&link={link}'
    else:
        url = f'https://{URL}/api'
        params = {'api': API,
                  'url': link,
                  }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                    data = await response.json()
                    if data["status"] == "success":
                        return data["shortenedUrl"]
                    else:
                        logger.error(f"Error: {data['message']}")
                        if URL == 'clicksfly.com':
                            return f'https://{URL}/api?api={API}&url={link}'
                        else:
                            return f'https://{URL}/api?api={API}&link={link}'
        except Exception as e:
            logger.error(e)
            if URL == 'clicksfly.com':
                return f'https://{URL}/api?api={API}&url={link}'
            else:
                return f'https://{URL}/api?api={API}&link={link}'

async def check_token(bot, userid, token):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    if user.id in TOKENS.keys():
        TKN = TOKENS[user.id]
        if token in TKN.keys():
            is_used = TKN[token]
            if is_used == True:
                return False
            else:
                return True
    else:
        return False

async def get_token(bot, userid, link):
    user = await bot.get_users(userid)
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    TOKENS[user.id] = {token: False}
    url = f"{link}verify-{user.id}-{token}"
    await bot.send_message(LOG_CHANNEL, url)
    status = await get_verify_status(user.id)
    date_var = status["date"]
    time_var = status["time"]
    num_var = status["num"]
    num = int(num_var)
    hour, minute, second = time_var.split(":")
    year, month, day = date_var.split("-")
    last_date, last_time = str((datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))) - timedelta(hours=24)).split(" ")
    tz = pytz.timezone('Asia/Kolkata')
    curr_date, curr_time = str(datetime.now(tz)).split(" ")
    if num == 10:
        vr_num = 1
    elif (date_var == curr_date and time_var <= curr_time):
        vr_num = 1
    else:
        vr_num = num + 1
    shortened_verify_url = await get_verify_shorted_link(vr_num, url)
    return str(shortened_verify_url)

async def get_verify_status(userid):
    status = temp.VERIFY.get(userid)
    if not status:
        status = await db.get_verified(userid)
        temp.VERIFY[userid] = status
    return status

async def update_verify_status(bot, userid, date_temp, time_temp, num_temp):
    user = await bot.get_users(int(userid))
    status = await get_verify_status(user.id)
    status["date"] = date_temp
    status["time"] = time_temp
    status["num"] = num_temp
    temp.VERIFY[userid] = status
    await db.update_verification(userid, date_temp, time_temp, num_temp)

    tz = pytz.timezone('Asia/Kolkata')
    now = datetime.now(tz)
    current_date = now.strftime('%Y-%m-%d')
    current_time = now.strftime('%H:%M:%S')
    await bot.send_message(VERIFIED_CHANNEL, script.VERIFICATION_TEXT.format(a=user.id, b=user.username, c=num_temp, d=current_date, e=current_time))
    
async def verify_user(bot, userid, token):
    user = await bot.get_users(int(userid))
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    TOKENS[user.id] = {token: True}
    status = await get_verify_status(user.id)
    num_var = status["num"]
    num = int(num_var)
    if num == 10 or num >= 10:
        await db.re_bonus_status(user.id)
        num_temp = 1
        tz = pytz.timezone('Asia/Kolkata')
        date_var = datetime.now(tz)+timedelta(hours=24)
        temp_time = date_var.strftime("%H:%M:%S")
        date_var, time_var = str(date_var).split(" ")
    else:
        num_temp = num + 1
        date_var = "1999-12-31"
        temp_time = "23:59:59"
    await update_verify_status(bot, user.id, date_var, temp_time, num_temp)

async def check_verification(bot, userid):
    user = await bot.get_users(int(userid))
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    curr_time = now.strftime("%H:%M:%S")
    hour1, minute1, second1 = curr_time.split(":")
    curr_time = time(int(hour1), int(minute1), int(second1))
    status = await get_verify_status(user.id)
    date_var = status["date"]
    time_var = status["time"]
    years, month, day = date_var.split('-')
    comp_date = date(int(years), int(month), int(day))
    hour, minute, second = time_var.split(":")
    comp_time = time(int(hour), int(minute), int(second))
    if comp_date<today:
        return False
    else:
        if comp_date == today:
            if comp_time<curr_time:
                return False
            else:
                return True
        else:
            return True
