import os
import importlib.util
from pyrogram import Client, filters


def get_command_list(module_path):
    command_list = []
    try:
        spec = importlib.util.spec_from_file_location("module.name", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        for name, obj in vars(module).items():
            if callable(obj) and hasattr(obj, "filters"):
                for filter in obj.filters:
                    if isinstance(filter, filters.command):
                        command_list.append(filter.commands)
    except Exception as e:
        print(f"Error loading commands from {module_path}: {e}")
    return command_list


def extract_commands_from_plugins_folder(folder_path):
    commands = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            module_path = os.path.join(folder_path, filename)
            command_list = get_command_list(module_path)
            commands.extend(command_list)
    return commands


@Client.on_message(filters.command("show_commands"))
async def show_commands(client, message):
    commands = extract_commands_from_plugins_folder("plugins")
    flattened_commands = [cmd for sublist in commands for cmd in sublist]
    if flattened_commands:
        await message.reply_text(f"Available Commands:\n\n" + "\n".join(flattened_commands))
    else:
        await message.reply_text("No commands found.")
