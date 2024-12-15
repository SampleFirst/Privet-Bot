import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS
from utils import is_subscribed, temp, get_size, check_verification, get_token, check_token, verify_user
from Script import script
import time
import datetime
import pytz

logger = logging.getLogger(__name__)



@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(a=message.from_user.id, b=message.from_user.username, c=message.from_user.mention))
    if len(message.command) != 2:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(user=message.from_user.mention),
            parse_mode=enums.ParseMode.HTML,
            quote=True
        )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [[InlineKeyboardButton("Join Our Back-Up Channel", url=invite_link.invite_link)]]
        await client.send_message(
            chat_id=message.from_user.id,
            text=f"**Hello {message.from_user.mention}, Due to overload only my channel subscribers can use me.\n\nPlease join my channel and then start me again!...**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN,
            quote=True
        )
        return
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(user=message.from_user.mention),
            parse_mode=enums.ParseMode.HTML,
            quote=True
        )
    data = message.command[1]
    if data == "start":
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(user=message.from_user.mention),
            parse_mode=enums.ParseMode.HTML,
            quote=True
        )
    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            await message.reply_text(
                text=f"<b>Hey {message.from_user.mention}, You are successfully verified !\nNow you have unlimited access for all movies till next 12 Hours.</b>",
                protect_content=True
            )
            await verify_user(client, userid, token)
        else:
            return await message.reply_text(
                text="<b>Invalid link or Expired link !</b>",
                protect_content=True
            )
                
@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))
        
@Client.on_message(filters.command('stats') & filters.incoming)
async def get_stats(bot, message):
    rju = await message.reply('Fetching stats..')
    try:
        total_users = await db.total_users_count()
        size = await db.get_db_size()
        free = 536870912 - size
        size = get_size(size)
        free = get_size(free)
        
        stats_message = (
            f"**Bot Stats**\n\n"
            f"**Total Users:** {total_users}\n"
            f"**Database Size:** {size}\n"
            f"**Free Space:** {free}"
        )
        await rju.edit(stats_message)
    except Exception as e:
        await rju.edit(f"An error occurred: {e}")


@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    raju = await message.reply('Getting List Of Users')
    users = await db.get_all_users()
    out = "Users Saved In DB Are:\n\n"
    async for user in users:
        user_id = user['id']
        out += f"<a href=tg://user?id={user_id}>{user['name']}</a>"
        if user['ban_status']['is_banned']:
            out += '( Banned User )'
        out += '\n'
    try:
        await raju.edit_text(out)
    except MessageTooLong:
        with open('users.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('users.txt', caption="List Of Users")

@Client.on_message(filters.command('deleteusers') & filters.user(ADMINS))
async def deleteusers(bot, message):
    msg = await message.reply('Starting deletion of users...')
    total_users = await db.total_users_count()
    start_time = time.time()
    count = 0
    complete = 0
    
    users = await db.get_all_users()
    async for user in users:
        try:
            print(user)
            user_id = user['id']  # Update this to match the correct key
            await db.delete_user(user_id)
            count += 1
            complete += 1
            
            if not complete % 20:
                await msg.edit(f"Total Users: {total_users}\nTotal Deleted: {complete}\nTotal Deletion Percentage: {complete / total_users * 100:.2f}%")
        
        except KeyError as e:
            await msg.edit(f"KeyError: {e}. User object: {user}")
            continue  # Skip this user and continue with the next
    
    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await msg.edit(f"All users deleted.\nTime taken: {time_taken}")
    
