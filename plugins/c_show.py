import os
import re
from pyrogram import Client, filters
from pyrogram.types import Message


# Function to extract 'filters.command' from a given file
def extract_commands_from_file(file_path):
    commands = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(r'filters\.command\(["\'](\w+)["\']', line)
            if match:
                commands.Clientend(match.group(1))
    return commands

# Command handler to search the repository for 'filters.command' and return them in a list
@Client.on_message(filters.command("list_commands"))
async def list_filters_commands(client: Client, message: Message):
    repo_path = "plugins"  # Set the path to your repository here
    all_commands = []

    # Walk through the repo and look for .py files
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                all_commands.extend(extract_commands_from_file(file_path))

    # Remove duplicates and sort the commands
    unique_commands = sorted(set(all_commands))

    # Send the list of commands as a message
    await message.reply_text("\n".join(unique_commands))


    
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

