from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from database.users_chats_db import db 


async def get_user_list(page, sort_by):
    users_cursor = await db.get_all_users()
    users = await users_cursor.to_list(length=None)

    if sort_by == "highest":
        users = sorted(users, key=lambda x: x['coins'], reverse=True)
    elif sort_by == "lowest":
        users = sorted(users, key=lambda x: x['coins'])
    
    start_index = (page - 1) * 10
    end_index = start_index + 10
    total_coins = sum(user['coins'] for user in users) + (200 * len(users))
    return users[start_index:end_index], len(users), total_coins

@Client.on_message(filters.command("show_users"))
async def show_users(client, message):
    page = 1
    sort_by = "default"
    user_list, total_users, total_coins = await get_user_list(page, sort_by)
    
    text = f"Total Users: {total_users}\nTotal Coins Earned: {total_coins}\n\n"
    text += "\n".join([f"<code>{i}. {user['name']} : {user['coins']} 🌑</code>" for i, user in enumerate(user_list, start=(page - 1) * 10 + 1)])
    
    keyboard = []
    if page > 1:
        keyboard.append(InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"))
    if len(user_list) == 10:
        keyboard.append(InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}"))
    keyboard = [keyboard]
    
    sort_buttons = [
        InlineKeyboardButton(f"Sort by Highest Coins{' ✅' if sort_by == 'highest' else ''}", callback_data="sort_highest"),
        InlineKeyboardButton(f"Sort by Lowest Coins{' ✅' if sort_by == 'lowest' else ''}", callback_data="sort_lowest")
    ]
    keyboard.append(sort_buttons)
    await message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))
