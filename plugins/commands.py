import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS
from utils import is_subscribed
from datetime import date, datetime
from Script import script
import pytz

logger = logging.getLogger(__name__)

buttonz = ReplyKeyboardMarkup(
    [
        ["Balance 💰", "🗣 Referral"],
        ["Bonus 🎁", "📤 Withdraw"]
    ],
    resize_keyboard=True
)

invite_url = ""


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

@Client.on_message(filters.regex('Balance 💰') & filters.private)
async def balance(bot, message):
    user = await db.get_user(message.from_user.id)
    username = message.from_user.username or "N/A"
    wallet = user.get("wallet", "None")
    balance = user.get("balance", 0)
    await message.reply(
        f"🆔 User: {username}\n\n📝 Wallet: {wallet}\n\n💳 Balance: {balance} Coins",
        quote=True
    )

@Client.on_message(filters.regex('🗣 Referral') & filters.private)
async def referral(bot, message):
    user_id = message.from_user.id
    bot_name = (await bot.get_me()).username
    total_referrals = await db.get_total_referrals(user_id)
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
        
# Define a command handler to store the invite URL
@Client.on_message(filters.command("store_url") & filters.private)
def store_invite_url(client, message):
    global invite_url
    
    command_parts = message.text.split("/store_url ", 1)
    text = command_parts[1]
    
    # Check if the text contains a Telegram invite URL
    if "https://t.me/" in text:
        invite_url = text
        message.reply_text(f"Invite URL stored: {invite_url}")
    else:
        message.reply_text("No valid Telegram invite URL found in the message.")

# Define a command handler to get the stored invite URL
@Client.on_message(filters.command("get_url") & filters.private)
def get_invite_url(client, message):
    global invite_url
    
    if invite_url:
        message.reply_text(f"Stored Invite URL: {invite_url}")
    else:
        message.reply_text("No URL has been stored yet.")

