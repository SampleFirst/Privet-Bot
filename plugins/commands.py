import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, REFER_ON, DAILY_BONUS, MYSTORE 
from utils import is_subscribed, temp, get_size, check_verification, get_token, check_token
from Script import script
import time
import datetime
import pytz

logger = logging.getLogger(__name__)

async def get_buttons(user_id):
    buttons = []
    settings = await db.get_settings()
    row = ["Balance 💰", "🗣 Referral"] if settings['refer_on'] else ["Balance 💰"]
    buttons.append(row)
    
    bonus = await db.get_bonus_status(user_id)
    if bonus["got_bonus"]:
        buttons.append(["Earn Coins 💵"])
    else:
        buttons.append(["Bonus 🎁"])
    
    user_coins = await db.get_coins(user_id)
    if settings["mystore"] or user_coins >= 100:
        buttons[-1].append("My Store 🛒")

    # Flatten the buttons list
    flat_buttons = [btn for row in buttons for btn in row]

    # Arrange buttons according to the new format
    if len(flat_buttons) == 1:
        arranged_buttons = [[flat_buttons[0]]]
    elif len(flat_buttons) == 2:
        arranged_buttons = [[flat_buttons[0], flat_buttons[1]]]
    elif len(flat_buttons) == 3:
        arranged_buttons = [[flat_buttons[0], flat_buttons[1]], [flat_buttons[2]]]
    elif len(flat_buttons) >= 4:
        arranged_buttons = [[flat_buttons[0], flat_buttons[1]], [flat_buttons[2], flat_buttons[3]]]
    
    return ReplyKeyboardMarkup(arranged_buttons, resize_keyboard=True)


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    user_exists = await db.is_user_exist(message.from_user.id)
    if not user_exists:
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(a=message.from_user.id, b=message.from_user.username, c=message.from_user.mention))

    buttonz = await get_buttons(message.from_user.id)

    if len(message.command) != 2:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TEXT.format(user=message.from_user.mention),
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
            text=script.FORCESUB_TEXT.format(user=message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.MARKDOWN,
            quote=True
        )
        return

    data = message.command[1]
    if data in ["subscribe", "error", "okay", "help"]:
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TEXT.format(user=message.from_user.mention),
            reply_markup=buttonz,
            parse_mode=enums.ParseMode.HTML,
            quote=True
        )
        return

    if data.startswith("verify"):
        userid, token = data.split("-", 2)[1], data.split("-", 3)[2]
        if str(message.from_user.id) != str(userid):
            await message.reply_text(text="<b>Invalid or Expired Link!</b>")
            return

        is_valid = await check_token(client, userid, token)
        if is_valid:
            await db.add_coins(userid, 20)
            await message.reply_text(text="Hey user You are successful verification")
        else:
            await message.reply_text(text="<b>Invalid or Expired Link!</b>")
        return

    if data.startswith("refer"):
        user_id = int(data.split("-", 1)[1])
        if await db.is_user_exist(user_id):
            if user_exists:
                await client.send_message(user_id, "ʏᴏᴜʀ ꜰʀɪᴇɴᴅ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴜꜱɪɴɢ ᴏᴜʀ ʙᴏᴛ")
            else:
                await client.send_message(user_id, "Congrats! You Won 10GB Upload limit")
        return
        

@Client.on_message((filters.command("balance") | filters.regex('Balance 💰')) & filters.private)
async def balance(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    balance = await db.get_coins(user_id)
    refer = await db.get_referral(user_id)
    await message.reply_text(
        text=script.BALANCE_TEXT.format(username=username, refer=refer, balance=balance),
        quote=True
    )

@Client.on_message((filters.command("referral") | filters.regex('🗣 Referral')) & filters.private)
async def referral(bot, message):
    settings = await db.get_settings()
    user_id = message.from_user.id
    user = message.from_user.first_name
    
    if settings['refer_on']:
        total_referrals = await db.get_referral(user_id)
        referral_link = f"https://telegram.me/{temp.U_NAME}?start=refer-{user_id}"
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Share Your Link", url=f"https://t.me/share/url?url={referral_link}")
                ]
            ]
        )
        await message.reply_text(
            text=script.REFER_TEXT.format(user=user, total_referrals=total_referrals),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
    else:
        buttonz = await get_buttons(message.from_user.id)
        msg = await message.reply_text(
            text=script.REFEROFF_TEXT.format(user=user),
            reply_markup=buttonz,
            quote=True
        )
        await asyncio.sleep(5)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[msg.id, message.id])


@Client.on_message((filters.command("bonus") | filters.regex('Bonus 🎁')) & filters.private)
async def bonus(bot, message):
    user_id = message.from_user.id
    user = message.from_user.first_name
    username = message.from_user.username or "N/A"
    bonus = await db.get_bonus_status(user_id)
    if bonus["got_bonus"] == True:
        buttonz = await get_buttons(user_id)
        await message.reply_text(
            text=script.BONUSOFF_TEXT.format(user=user),
            reply_markup=buttonz,
            quote=True
        )
        await bot.send_message(LOG_CHANNEL, script.BONUSFLOOD_TEXT.format(user_id=user_id, username=username))
    else:
        await db.got_bonus_status(user_id)
        await db.add_coins(user_id, 10)
        buttonz = await get_buttons(user_id)
        await message.reply_text(
            text=script.BONUS_TEXT.format(user=user),
            reply_markup=buttonz,
            quote=True
        )

@Client.on_message((filters.command("earn_coins") | filters.regex('Earn Coins 💵')) & filters.private)
async def earn_coins(client, message):
    user = message.from_user.mention
    try:
        if not await check_verification(client, message.from_user.id):
            btn = [[
                InlineKeyboardButton(f"Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=")),
                InlineKeyboardButton("How To Verify", url="https://t.me/+IvrcMfPKCMxkNjVl")
            ]]
            await client.send_message(
                chat_id=message.from_user.id,
                text=script.EARNCOIN_TEXT.format(user=user),
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            return
        else:
            await client.send_message(
                chat_id=message.from_user.id,
                text=script.EARNCOINS_TEXT.format(user=user)
            )
    except Exception as e:
        await message.reply(str(e))
        
@Client.on_message((filters.command("mystore") | filters.regex('My Store 🛒')) & filters.private)
async def mystore(bot, message):
    try:
        await message.reply_text(
            text=script.MYSTORE_TEXT.format(),
            quote=True
        )
    except Exception as e:
        await message.reply(str(e))
        
@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    try:
        await message.reply_document('Logs.txt')
    except Exception as e:
        await message.reply(str(e))

# Handle the /help command
@Client.on_message(filters.command("help"))
async def help(client, message):
    try:
        user = message.from_user.first_name
        await message.reply_text(
            text=script.HELP_TEXT.format(user=user),
            quote=True
        )
    except Exception as e:
        await message.reply(str(e))
        
# Handle the /about command
@Client.on_message(filters.command("about"))
async def about(client, message):
    try:
        user = message.from_user.first_name
        await message.reply_text(
            text=script.ABOUT_TEXT.format(user=user),
            quote=True
        )
    except Exception as e:
        await message.reply(str(e))
    
@Client.on_message(filters.command('stats') & filters.incoming)
async def get_stats(bot, message):
    msg = await message.reply('Fetching stats..')
    try:
        total_users = await db.total_users_count()
        size = await db.get_db_size()
        free = 536870912 - size
        size = get_size(size)
        free = get_size(free)
        
        await msg.edit(script.STATS_TEXT.format(total_users=total_users, size=size, free=free))
    except Exception as e:
        await msg.edit(f"An error occurred: {e}")

@Client.on_message(filters.command('users') & filters.user(ADMINS))
async def list_users(bot, message):
    try:
        msg = await message.reply('Getting List Of Users')
        users = await db.get_all_users()
        out = "Users Saved In DB Are:\n\n"
        async for user in users:
            out += f"<a href=tg://user?id={user['id']}>{user['name']}</a>"
            if user['ban_status']['is_banned']:
                out += '( Banned User )'
            out += '\n'
        try:
            await msg.edit_text(out)
        except MessageTooLong:
            with open('users.txt', 'w+') as outfile:
                outfile.write(out)
            await message.reply_document('users.txt', caption="List Of Users")
    except Exception as e:
        await msg.edit(f"An error occurred: {e}")
        
@Client.on_message(filters.command('deleteusers') & filters.user(ADMINS))
async def deleteusers(bot, message):
    try:
        await db.delete_all_users()
        await message.reply("All user have been deleted.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@Client.on_message(filters.command('settings'))
async def settings(client, message):
    settings = await db.get_settings()
    if settings is not None:
        buttons = [
            [
                InlineKeyboardButton('Refer Earn', callback_data="refer"),
                InlineKeyboardButton('✅ ON' if settings["refer_on"] else '❌ OFF', callback_data="toggle_refer")
            ],
            [
                InlineKeyboardButton('Daily Bonus', callback_data="bonus"),
                InlineKeyboardButton('✅ ON' if settings["daily_bonus"] else '❌ OFF', callback_data="toggle_bonus")
            ],
            [
                InlineKeyboardButton('My Store', callback_data="store"),
                InlineKeyboardButton('✅ Always ON' if settings["mystore"] else '❌ After Earn', callback_data="toggle_store")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=f"<b>Change Your Settings ⚙</b>",
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.HTML,
            reply_to_message_id=message.id
        )

@Client.on_message(filters.command("get_settings") & filters.user(ADMINS))
async def get_settings(client, message):
    try:
        settings = await db.get_all_settings()
        if not settings:
            await message.reply("No settings found.")
            return
        settings_str = "\n".join([f"{key}: {value}" for key, value in settings.items()])
        await message.reply(f"Current settings:\n{settings_str}")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

@Client.on_message(filters.command("delete_settings") & filters.user(ADMINS))
async def delete_settings(client, message):
    try:
        await db.delete_all_settings()
        await message.reply("All settings have been deleted.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")
