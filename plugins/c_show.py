import os
from pyrogram import Client, filters


@Client.on_message(filters.command("list_commands"))
async def list_commands(client, message):
    repo_path = "/path/to/your/repo"  # specify the path to your deployed repo

    # Walk through the repo directory
    commands = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):  # adjust this filter based on the file types you want to include
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip().startswith('@Client.on_message'):
                            command = line.strip()
                            commands.append(command)

    # Send the list of commands as a message
    if commands:
        response = "List of commands found in the repo:\n\n" + "\n".join(commands)
    else:
        response = "No commands found in the repo."

    await message.reply_text(response)


@Client.on_message(filters.command("show_commands"))
async def show_commands(client, message):
    # Get the argument from the message (assuming the format is /list_commands <repo_path>)
    if len(message.command) < 2:
        await message.reply_text("Please provide the repository path. Usage: /list_commands repo_path")
        return

    repo_path = message.command[1]

    # Check if the path exists
    if not os.path.exists(repo_path):
        await message.reply_text("The specified path does not exist. Please provide a valid path.")
        return

    # Walk through the repo directory
    commands = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):  # adjust this filter based on the file types you want to include
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.strip().startswith('@Client.on_message'):
                            command = line.strip()
                            commands.append(command)

    # Send the list of commands as a message
    if commands:
        response = "List of commands found in the repo:\n\n" + "\n".join(commands)
    else:
        response = "No commands found in the repo."

    await message.reply_text(response)
    
