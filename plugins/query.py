from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.users_chats_db import db
from info import ADMINS


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    qdata = query.data.split("_")
    if query.data == "close_data":
        await query.message.delete()
    
    elif qdata[0] == "prev" or qdata[0] == "next":
        page = int(qdata[1])
        sort_by = qdata[2]
        if qdata[0] == "prev":
            page = max(1, page - 1)
        elif qdata[0] == "next":
            page += 1
        
        user_list, total_users = await get_user_list(page, sort_by)
        text = "\n".join([f"{user['name']} - Coins: {user['coins']}" for user in user_list])
        
        keyboard = [
            [InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"), InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}")],
            [InlineKeyboardButton("Sort by Highest Coins", callback_data="sort_highest"), InlineKeyboardButton("Sort by Lowest Coins", callback_data="sort_lowest")]
        ]
        
        await callback_query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif qdata[0] == "sort":
        sort_by = qdata[1]
        page = 1
        user_list, total_users = await get_user_list(page, sort_by)
        
        text = "\n".join([f"{user['name']} - Coins: {user['coins']}" for user in user_list])
        
        keyboard = [
            [InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"), InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}")],
            [InlineKeyboardButton("Sort by Highest Coins", callback_data="sort_highest"), InlineKeyboardButton("Sort by Lowest Coins", callback_data="sort_lowest")]
        ]
        
        await callback_query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith('toggle_'):
        setting = query.data.split('_')[1]
        settings = await db.get_settings()
        if setting == "refer":
            settings['refer_on'] = not settings.get('refer_on', False)
        elif setting == "bonus":
            settings['daily_bonus'] = not settings.get('daily_bonus', False)
        elif setting == "store":
            settings['mystore'] = not settings.get('mystore', False)
        
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
                InlineKeyboardButton('My Store', callback_data="store"),
                InlineKeyboardButton('✅ Always ON' if settings["mystore"] else '❌ After Earn', callback_data="toggle_store")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_reply_markup(reply_markup=reply_markup)
        
    elif query.data == "confirm_reset":
        rju = await query.message.edit("Resetting database...")
        try:
            await db.reset_database()
            await rju.edit("Database has been reset successfully.")
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            await rju.edit(f"An error occurred while resetting the database: {e}")
    elif query.data == "cancel_reset":
        await query.message.edit("Database reset has been canceled.")
    elif query.data == "testing":
        await query.message.edit("You have selected the testing option.")

