import os
import logging
import random
import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from database.users_chats_db import db
from info import ADMINS, AUTH_CHANNEL, LOG_CHANNEL, PICS, REFER_ON, DAILY_BONUS, WITHDRAW_BTN
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
        buttons.append(["Earn Credits 💵"])
    else:
        buttons.append(["Bonus 🎁"])
    
    user_credits = await db.get_credits(user_id)
    if settings["withdraw_btn"] or user_credits >= 100:
        buttons[-1].append("📤 Withdraw")

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
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(a=message.from_user.id, b=message.from_user.username, c=message.from_user.mention))
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
        settings = await db.get_settings()
        if settings['refer_on']:
            id = message.text.split(' ')[1]
            if id:
                if not await db.is_user_exist(message.from_user.id):
                    await db.add_user(message.from_user.id, message.from_user.first_name, id)
                    await client.send_message(id, "Congrats! You Won 10GB Upload limit")
                else:
                    await client.send_message(id, "ʏᴏᴜʀ ꜰʀɪᴇɴᴅ ɪꜱ ᴀʟʀᴇᴀᴅʏ ᴜꜱɪɴɢ ᴏᴜʀ ʙᴏᴛ")
        else:
            return 

@Client.on_message(filters.regex('Balance 💰') & filters.private)
async def balance(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    balance = await db.get_credits(user_id)
    await message.reply(
        f"🆔 User: {username}\n\n💳 Credits: {balance} ",
        quote=True
    )

@Client.on_message(filters.regex('🗣 Referral') & filters.private)
async def referral(bot, message):
    settings = await db.get_settings()
    user_id = message.from_user.id
    
    if settings['refer_on']:
        total_referrals = await db.get_referral(user_id)
        referral_link = f"https://t.me/{temp.U_NAME}?start={user_id}"
        await message.reply(
            f"💰 Per Refer: Upto 50 Coins\n\n📝 Total Referrals: {total_referrals}\n\n🔍 Your Referral Link: {referral_link}",
            disable_web_page_preview=True,
            quote=True
        )
    else:
        buttonz = await get_buttons(message.from_user.id)
        msg = await message.reply(
            text="Referral program is currently disabled.",
            reply_markup=buttonz,
            quote=True
        )
        await asyncio.sleep(5)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=[msg.id, message.id])


@Client.on_message(filters.regex('Bonus 🎁') & filters.private)
async def bonus(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    bonus = await db.get_bonus_status(user_id)
    if bonus["got_bonus"] == True:
        buttonz = await get_buttons(user_id)
        await message.reply(
            "🎁 Your already Received 20 Credits", 
            reply_markup=buttonz,
            quote=True
        )
        await bot.send_message(LOG_CHANNEL, f"Hey Admin {user_id} Name: {username} Try Again For Bonus")
    else:
        await db.got_bonus_status(user_id)
        await db.add_credits(user_id, 20)
        buttonz = await get_buttons(user_id)
        await message.reply(
            "🎁 Congratulation, you Received 20 Credits", 
            reply_markup=buttonz,
            quote=True
        )

@Client.on_message(filters.regex('Earn Credits 💵') & filters.private)
async def earn_credits(client, message):
    if not await check_verification(client, message.from_user.id):
        btn = [[
            InlineKeyboardButton(f"Verify", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=")),
            InlineKeyboardButton("How To Verify", url="https://t.me/+IvrcMfPKCMxkNjVl")
        ]]
        await client.send_message(
            chat_id=message.from_user.id,
            text=f"Hey {message.from_user.mention} 💕\n\nComplete This Ad And Earn 20 Credits.",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(btn)
        )
        return
    else:
        await client.send_message(
            chat_id=message.from_user.id,
            text="Congratulations! You've reached the daily credits limit set by our credits management system, Please try again after 24 hours."
        )

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
            user_id = user['id']
            await db.delete_user(user_id)
            count += 1
            complete += 1
            
            if not complete % 20:
                await msg.edit(f"Total Users: {total_users}\nTotal Deleted: {complete}\nTotal Deletion Percentage: {complete / total_users * 100:.2f}%")
        
        except KeyError as e:
            await msg.edit(f"KeyError: {e}. User object: {user}")
            continue
    
    time_taken = datetime.timedelta(seconds=int(time.time() - start_time))
    await msg.edit(f"All users deleted.\nTime taken: {time_taken}")
    
@Client.on_message(filters.command("set_setting") & filters.user(ADMINS))
async def set_setting(client, message):
    try:
        args = message.text.split(None, 2)
        if len(args) < 3:
            await message.reply("Usage: /set_setting <key> <value>")
            return
        key = args[1]
        value = args[2]
        await db.add_setting(key, value)
        await message.reply(f"Setting `{key}` has been updated to `{value}`.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

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
                InlineKeyboardButton('Withdraw BTN', callback_data="withdraw"),
                InlineKeyboardButton('✅ Always ON' if settings["withdraw_btn"] else '❌ After 100 Coins', callback_data="toggle_withdraw")
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

@Client.on_callback_query(filters.regex('toggle_'))
async def toggle_settings(client, callback_query):
    setting = callback_query.data.split('_')[1]
    settings = await db.get_settings()
    if setting == "refer":
        settings['refer_on'] = not settings.get('refer_on', False)
    elif setting == "bonus":
        settings['daily_bonus'] = not settings.get('daily_bonus', False)
    elif setting == "withdraw":
        settings['withdraw_btn'] = not settings.get('withdraw_btn', False)
        
    await db.update_settings(settings)
    
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
            InlineKeyboardButton('Withdraw BTN', callback_data="withdraw"),
            InlineKeyboardButton('✅ Always ON' if settings["withdraw_btn"] else '❌ After Earn', callback_data="toggle_withdraw")
        ],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await callback_query.message.edit_reply_markup(reply_markup=reply_markup)
