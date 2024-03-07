from pyrogram import Client, filters
from datetime import datetime
from plugins.status_name import get_status_name
from database.users_chats_db import db

@Client.on_message(filters.command("myplan"))
async def myplan(_, message):
    if message.chat.type == "private":
        await message.reply("This command can only be used in groups or channels.")
        return
    
    bot_names = ["Movies Bot", "File to Link Bot", "Rename Bot", "YouTube Downloader Bot"]
    db_names = ["Movies Database", "Anime Database", "Series Database", "Audio Book Database"]
    now_status = get_status_name(status_num=3)
    bot_statuses = await db.get_verified_dot(message.chat.id, bot_names, now_status)
    db_statuses = await db.get_verified_bd(message.chat.id, db_names, now_status)

    response = "Premium status:\n\n"
    
    if bot_statuses:
        response += "Active Premium Bots:\n"
        for bot_status in bot_statuses:
            response += f"Bot Name: {bot_status.get('bot_name')}\n"
            response += f"Now Status: {bot_status.get('now_status')}\n"
            response += f"Activate Datetime: {datetime.fromtimestamp(bot_status.get('date')).strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"Expire Datetime: {datetime.fromtimestamp(bot_status.get('time')).strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    if db_statuses:
        response += "Active Premium Databases:\n"
        for db_status in db_statuses:
            response += f"Database Name: {db_status.get('db_name')}\n"
            response += f"Now Status: {db_status.get('now_status')}\n"
            response += f"Activate Datetime: {datetime.fromtimestamp(db_status.get('date')).strftime('%Y-%m-%d %H:%M:%S')}\n"
            response += f"Expire Datetime: {datetime.fromtimestamp(db_status.get('time')).strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    if not bot_statuses and not db_statuses:
        response = "No premium status found for this group or channel."
    
    await message.reply(response)
