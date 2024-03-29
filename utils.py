import logging
import pytz
from datetime import date, time, datetime, timedelta
from pyrogram import Client, filters, enums
from database.users_chats_db import db
from info import AUTH_CHANNEL, LOG_CHANNEL, PREMIUM_LOGS, PAYMENT_CHAT, MOVIES_DB, ANIME_DB, SERIES_DB, AUDIOBOOK_DB

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Temp DB for banned
class temp(object):
    STATUS_BOT = {}
    STATUS_DB = {}
    
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

async def get_timedelta(now_status):
    if now_status == "is Attempt":
        return timedelta(minutes=2)
    elif now_status == "is Confirm":
        return timedelta(minutes=2)
    elif now_status == "is Premium":
        return timedelta(days=30)
    elif now_status == "Attempt Cancel":
        return timedelta(minutes=2)
    elif now_status == "Confirm Cancel":
        return timedelta(minutes=2)
    elif now_status == "Premium Cancel":
        return timedelta(minutes=2)
    elif now_status == "Attempt expired":
        return timedelta(minutes=1)
    elif now_status == "Confirm expired":
        return timedelta(minutes=1)
    elif now_status == "Premium expired":
        return timedelta(minutes=1)
    elif now_status == "Attempt Remove":
        return timedelta(minutes=1)
    elif now_status == "Confirm Remove":
        return timedelta(minutes=1)
    elif now_status == "Premium Remove":
        return timedelta(minutes=1)
    else:
        raise ValueError("Invalid now_status. Please choose a valid status.")

async def send_invite_link(client, user_id, db_name):
    database_channels = {
        "Movies Database": MOVIES_DB,
        "Anime Database": ANIME_DB,
        "Series Database": SERIES_DB,
        "Audio Book Database": AUDIOBOOK_DB
    }
    
    try:
        channel_ids = database_channels[db_name]
        for channel_id in channel_ids:
            total_members = await client.get_chat_members_count(channel_id)
            if total_members < 50:
                tz = pytz.timezone('Asia/Kolkata')
                invite_expire = datetime.now(tz) + timedelta(minutes=2)
                
                link = await client.create_chat_invite_link(
                    int(channel_id),
                    expire_date=invite_expire,
                    member_limit=1
                )

                invite_link_count = 1

                await client.send_message(user_id, f"Congratulations, you've been upgraded to Premium for {db_name}! 🌟 Here is your invite link:\n{link.invite_link} 🚀", parse_mode=enums.ParseMode.HTML)
                await db.store_invite_link(user_id, db_name, channel_id, link.invite_link, invite_link_count, invite_expire)
                logger.info(f"{user_id} update status for {db_name} with {channel_id} and {link.invite_link} and {invite_link_count} and {invite_expire}")
                break
    except KeyError:
        await client.send_message(user_id, "Invalid database selected.")

async def update_verification(bot, user_id, name, now_status):
    user = await bot.get_users(int(user_id))
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
        await bot.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(user.id, user.mention))
    tz = pytz.timezone('Asia/Kolkata')
    delta = await get_timedelta(now_status)
    date_var = datetime.now(tz) + delta
    temp_time = date_var.strftime("%H:%M:%S")
    date_var, time_var = str(date_var).split(" ")
    status_key = f"{user_id}_{name}_{now_status}"
    print("Status key:", status_key)  # Print status key
    await update_verify_status(user.id, name, now_status, date_var, temp_time)

async def update_verify_status(user_id, name, now_status, date_temp, time_temp):
    status = await get_verify_status(user_id, name, now_status)
    status["date"] = date_temp
    status["time"] = time_temp
    status_key = f"{user_id}_{name}_{now_status}"
    if name == 'bot':
        temp.STATUS_BOT[status_key] = status
        await db.update_verification_dot(user_id, name, now_status, date_temp, time_temp)
    else:
        temp.STATUS_DB[status_key] = status
    await db.update_verification_bd(user_id, name, now_status, date_temp, time_temp)

async def get_verify_status(user_id, name, now_status):
    status_key = f"{user_id}_{name}_{now_status}"
    if name == 'bot':
        status = temp.STATUS_BOT.get(status_key)
    else:
        status = temp.STATUS_DB.get(status_key)
    if not status:
        if name == 'bot':
            status = await db.get_verified_dot(user_id, name, now_status)
        else:
            status = await db.get_verified_bd(user_id, name, now_status)
        if name == 'bot':
            temp.STATUS_BOT[status_key] = status
        else:
            temp.STATUS_DB[status_key] = status
    return status
    
async def check_verification(bot, user_id, name, now_status):
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
    status_key = f"{user_id}_{name}_{now_status}"
    print("Status key:", status_key)  # Print status key
    status = await get_verify_status(user_id, name, now_status)
    date_var = status.get("date")  # Use get() method to retrieve the value, returns None if key doesn't exist
    time_var = status.get("time")  # Use get() method to retrieve the value, returns None if key doesn't exist
    if date_var is None or time_var is None:
        return False
    years, month, day = date_var.split('-')
    comp_date = date(int(years), int(month), int(day))
    hour, minute, second = time_var.split(":")
    comp_time = time(int(hour), int(minute), int(second))
    if comp_date < today:
        return False
    else:
        if comp_date == today:
            if comp_time < curr_time:
                return False
            else:
                return True
        else:
            return True
