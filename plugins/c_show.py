import os
from pyrogram import Client, filters
import re

def get_commands():
    commands = []
    for file in os.listdir('plugins'):
        if file.endswith('.py'):
            command_name = file.replace('.py', '')
            commands.append(f'/{command_name}')
    return commands
    
@Client.on_message(filters.command("list_commands"))
async def list_filters_commands(client, message):
    commands = get_commands()
    response_text = 'Available commands:\n'
    for command in commands:
        response_text += f'{command}\n'
    await message.reply_text(response_text)
    
@Client.on_message(filters.command("list_filters"))
async def list_filters(client, message):
    filters_list = []
    for filter_name in dir(filters):
        if not filter_name.startswith("_"):
            filters_list.append(filter_name)
    await message.reply_text("List of all filters:\n" + "\n".join(filters_list))

@Client.on_message(filters.command("show_commands"))
def show_commands(client, message):
    commands = []
    
    # Check all attributes in Client class
    for attr_name in dir(client):
        attr = getattr(client, attr_name)
        
        # Ensure the attribute is callable and a command handler
        if callable(attr) and hasattr(attr, 'filters') and attr.filters:
            for filter_obj in attr.filters:
                if isinstance(filter_obj, filters.command):
                    commands.append(filter_obj.commands[0])
    
    # Construct the response message
    response = "Available commands:\n"
    for command in commands:
        response += f"/{command}\n"
    
    # Send the response message
    client.send_message(message.chat.id, response)


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

