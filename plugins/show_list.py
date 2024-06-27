from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from database.users_chats_db import db 

# Function to get user list with pagination and sorting
async def get_user_list(page, sort_by):
    users_cursor = await db.get_all_users()
    users = await users_cursor.to_list(length=100)  # Fetching all users for sorting and pagination

    if sort_by == "highest_coins":
        users = sorted(users, key=lambda x: x['coins'], reverse=True)
    elif sort_by == "lowest_coins":
        users = sorted(users, key=lambda x: x['coins'])
    
    start_index = (page - 1) * 10
    end_index = start_index + 10
    return users[start_index:end_index], len(users)

@Client.on_message(filters.command("show_users"))
async def show_users(client, message):
    page = 1
    sort_by = "default"
    user_list, total_users = await get_user_list(page, sort_by)
    
    text = "\n".join([f"{user['name']} - Coins: {user['coins']}" for user in user_list])
    
    keyboard = [
        [InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"), InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}")],
        [InlineKeyboardButton("Sort by Highest Coins", callback_data="sort_highest"), InlineKeyboardButton("Sort by Lowest Coins", callback_data="sort_lowest")]
    ]

    await message.reply(text, reply_markup=InlineKeyboardMarkup(keyboard))

