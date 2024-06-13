import os
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import re

@Client.on_message(filters.command("list_filters"))
async def list_filters(client, message):
    filters_list = []
    for filter_name in dir(filters):
        if not filter_name.startswith("_"):
            filters_list.append(filter_name)
    await message.reply_text("List of all filters:\n" + "\n".join(filters_list))

@Client.on_message(filters.command("list_commands"))
async def listcommand(client, message):
    commands_list = []
    for handler in client.dispatcher.get_handlers_by_update_type("message"):
        if isinstance(handler, MessageHandler):
            command_filters = getattr(handler, 'filters', None)
            if command_filters and command_filters.commands:
                commands_list.extend(command_filters.commands)
    await message.reply_text("List of all commands:\n" + "\n".join(commands_list))

@Client.on_message(filters.command("commands"))
async def list_commands(client, message):
    repo_path = "plugins"  # specify the path to your deployed repo

    # Walk through the repo directory
    command_list = []
    button_list = []
    
    command_pattern = re.compile(r'filters\.command\("([^"]+)"\)')
    regex_pattern = re.compile(r'filters\.regex\(\'([^\']+)\'\)')

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                await message.reply_text(f"Searching commands in file `{file}`")
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        command_match = command_pattern.search(line)
                        regex_match = regex_pattern.search(line)
                        if command_match:
                            command_list.append(command_match.group(1))
                        if regex_match:
                            button_list.append(regex_match.group(1))

    # Format the response
    response = "Buttons list\n"
    if button_list:
        for idx, button in enumerate(button_list, 1):
            response += f"{idx}) <code>{button}</code>\n"
    else:
        response += "No buttons found.\n"

    response += "\nCommands list\n"
    if command_list:
        for idx, command in enumerate(command_list, 1):
            response += f"{idx}) /{command}\n"
    else:
        response += "No commands found."

    await message.reply_text(response)

