import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from database.users_chats_db import db 
from info import ADMINS 
from utils import extract_commands, get_user_list

@Client.on_message(filters.command("commands") & filters.user(ADMINS))
async def list_commands(client: Client, message: Message):
    repo_path = "plugins"
    all_commands = []
    for root, dirs, files in os.walk(repo_path):
        for file in sorted(files):
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_commands.extend(extract_commands(file_path))
    seen = set()
    unique_commands = []
    for command in all_commands:
        if command not in seen:
            seen.add(command)
            unique_commands.append(command)
    await message.reply_text("\n".join(f"/{command}" for command in unique_commands))

@Client.on_message(filters.command("show_users") & filters.user(ADMINS))
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

