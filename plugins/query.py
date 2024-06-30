from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.users_chats_db import db
from info import ADMINS
from plugins.show_list import get_user_list

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
        
        user_list, total_users, total_coins = await get_user_list(page, sort_by)
        text = f"Total Users: {total_users}\nTotal Coins Earned: {total_coins}\n\n"
        text += "\n".join([
            f"<code>{i}. {user['coins']} : {user['name']}</code>"
            for i, user in enumerate(user_list, start=(page - 1) * 10 + 1)
        ])
        
        keyboard = []
        if page > 1:
            keyboard.append(InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"))
        if len(user_list) == 10:  # Assuming 10 users per page
            keyboard.append(InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}"))
        keyboard = [keyboard]
        
        sort_buttons = [
            InlineKeyboardButton(f"Sort by Highest Coins{' ✅' if sort_by == 'highest' else ''}", callback_data="sort_highest"),
            InlineKeyboardButton(f"Sort by Lowest Coins{' ✅' if sort_by == 'lowest' else ''}", callback_data="sort_lowest")
        ]
        keyboard.append(sort_buttons)
        
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif qdata[0] == "sort":
        sort_by = qdata[1]
        page = 1
        user_list, total_users, total_coins = await get_user_list(page, sort_by)
        
        text = f"Total Users: {total_users}\nTotal Coins Earned: {total_coins}\n\n"
        text += "\n".join([
            f"<code>{i}. {user['coins']} : {user['name']}</code>"
            for i, user in enumerate(user_list, start=(page - 1) * 10 + 1)
        ])
        keyboard = []
        if page > 1:
            keyboard.append(InlineKeyboardButton("Previous", callback_data=f"prev_{page}_{sort_by}"))
        if len(user_list) == 10:  # Assuming 10 users per page
            keyboard.append(InlineKeyboardButton("Next", callback_data=f"next_{page}_{sort_by}"))
        keyboard = [keyboard]
        
        sort_buttons = [
            InlineKeyboardButton(f"Sort by Highest Coins{' ✅' if sort_by == 'highest' else ''}", callback_data="sort_highest"),
            InlineKeyboardButton(f"Sort by Lowest Coins{' ✅' if sort_by == 'lowest' else ''}", callback_data="sort_lowest")
        ]
        keyboard.append(sort_buttons)
        
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(keyboard))


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

