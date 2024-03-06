import logging
import pytz
from datetime import datetime, timedelta
from pyrogram import Client
from database.users_chats_db import db
from info import AUTH_CHANNEL, LOG_CHANNEL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Temp DB for banned
class temp(object):
    STATUS = {}
    
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


async def update_verification(bot, user_id, bot_name):
    user = await bot.get_users(int(user_id))
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    tz = pytz.timezone('Asia/Kolkata')
    date_var = datetime.now(tz) + timedelta(minutes=2)
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    status_key = f"{user_id}_{bot_name}"
    print("Status key:", status_key)  # Print status key
    await update_verify_status(user.id, status_key, date_var, temp_time)

async def update_verify_status(user_id, status_key, date_temp, time_temp):
    status = await get_verify_status(user_id, bot_name)
    status["date"] = date_temp
    status["time"] = time_temp
    temp.STATUS[status_key] = status
    await db.update_verification(user_id, bot_name, date_temp, time_temp)


async def get_verify_status(user_id, bot_name):
    status_key = f"{user_id}_{bot_name}"
    status = temp.STATUS.get(status_key)
    if not status:
        status = await db.get_verified(user_id, bot_name)
        temp.STATUS[status_key] = status
    return status
    
async def check_verification(bot, user_id, bot_name):
    user = await bot.get_users(int(user_id))
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    tz = pytz.timezone('Asia/Kolkata')
    today = date.today()
    now = datetime.now(tz)
    curr_time = now.strftime("%H:%M:%S")
    hour1, minute1, second1 = curr_time.split(":")
    curr_time = time(int(hour1), int(minute1), int(second1))
    status_key = f"{user_id}_{bot_name}"
    print("Status key:", status_key)  # Print status key
    status = await get_verify_status(user_id, bot_name)
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

