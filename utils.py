import logging
from datetime import datetime, timedelta
import pytz
from pyrogram import Client
from database.users_chats_db import db
from info import AUTH_CHANNEL, LOG_CHANNEL

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


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


async def check_status(client, userid, bot_name):
    user = await client.get_users(int(userid))
    tz = pytz.timezone('Asia/Kolkata')
    today = datetime.now(tz).date()
    now = datetime.now(tz).time()
    status = await db.get_status_bot(userid, bot_name)
    date_var = status["date"]
    time_var = status["time"]
    comp_date = datetime.strptime(date_var, '%Y-%m-%d').date()
    comp_time = datetime.strptime(time_var, '%H:%M:%S').time()
    if comp_date < today:
        return False
    elif comp_date == today:
        if comp_time < now:
            return False
        else:
            return True
    else:
        return True


async def update_status(client, user_id, bot_name):
    now_status = "is attempt"
    date = datetime.now().date()
    time = datetime.now().time()
    await db.update_status_bot(user_id, bot_name, now_status, date, time)
