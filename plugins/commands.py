import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, REFERRAL_ON
from utils import is_subscribed
from datetime import date, datetime
from Script import script
import pytz

logger = logging.getLogger(__name__)

async def get_buttons(user_id):
    buttons = [
        ["Balance 💰", "Bonus 🎁"]
    ]
    if REFERRAL_ON:
        buttons[0].insert(1, "🗣 Referral")
    user_credits = await db.get_credits(user_id)
    if user_credits >= 100:
        buttons[0].append("📤 Withdraw")
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [
            [
                InlineKeyboardButton('Support Chat', callback_data="none"),
                InlineKeyboardButton('Update Channel', callback_data="none")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await asyncio.sleep(2)
        if not await db.get_chat(message.chat.id):
            total = await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(a=message.chat.title, b=message.chat.id, c=message.chat.username, d=total, f=client.mention, e="Unknown"))
            await db.add_chat(message.chat.id, message.chat.title, message.chat.username)
        return
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention, message.from_user.username))
    buttonz = await get_buttons(message.from_user.id)
    if len(message.command) != 2:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(user=message.from_user.mention),
            reply_markup=buttonz,
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
            reply_markup=buttonz,
            parse_mode=enums.ParseMode.HTML,
            quote=True
        )
    data = message.command[1]    
    if data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Invalid or Expired Link!</b>"
            )
        is_valid = await check_token(client, userid, token)
        if is_valid:
            await db.add_credits(userid, 20)
            await message.reply_text(
                text="Hey user You are successful verification"
            )
            return
        else:
            return await message.reply_text(
                text="<b>Invalid or Expired Link!</b>"
            )
    else:
        id = message.text.split(' ')[1]
        if id:
            if not await db.is_user_exist(message.from_user.id):
                await db.add_user(message.from_user.id, message.from_user.first_name, id)
                await client.send_message(id, "Congrats! You Won 10GB Upload limit")
            else:
                await client.send_message(id, "ʏᴏᴜʀ ꜰʀɪᴇɴᴅ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴜꜱɪɴɢ ᴏᴜʀ ʙᴏᴛ")
                

@Client.on_message(filters.regex('Balance 💰') & filters.private)
async def balance(bot, message):
    user = await db.get_user(message.from_user.id)
    username = message.from_user.username or "N/A"
    balance = await db.get_credits(user.id)
    await message.reply(
        f"🆔 User: {username}\n\n💳 Credits: {balance} ",
        quote=True
    )

@Client.on_message(filters.regex('🗣 Referral') & filters.private)
async def referral(bot, message):
    user_id = message.from_user.id
    bot_name = (await bot.get_me()).username
    total_referrals = await db.get_referral(user_id)
    referral_link = f"https://t.me/{bot_name}?start={user_id}"
    await message.reply(
        f"💰 Per Refer: Upto 50 Coins\n\n📝 Total Referrals: {total_referrals}\n\n🔍 Your Referral Link: {referral_link}",
        parse_mode=enums.ParseMode.MARKDOWN,
        quote=True
    )
    
@Client.on_message(filters.regex('Bonus 🎁') & filters.private)
async def bonus(bot, message):
    await message.reply("🎁 You can earn bonus by participating in our events and activities!", quote=True)

@Client.on_message(filters.regex('📤 Withdraw') & filters.private)
async def withdraw(bot, message):
    await message.reply("📤 You can withdraw your balance once you reach the minimum threshold. Please contact support for more details.", quote=True)

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))
        
