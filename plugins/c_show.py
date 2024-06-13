import os
import importlib.util
from pyrogram import Client, filters


def get_command_list(module_path):
    command_list = []
    spec = importlib.util.spec_from_file_location("module.name", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name, obj in vars(module).items():
        if callable(obj) and hasattr(obj, "filters"):
            for filter in obj.filters:
                if isinstance(filter, filters.command):
                    command_list.append(filter.commands)
    return command_list

@Client.on_message(filters.command("show_commands"))
async def show_commands(client, message):
    command_list = get_command_list("plugins")  # Update with the correct path
    commands = [cmd for sublist in command_list for cmd in sublist]  # Flatten the list of lists
    await message.reply_text(f"Available Commands:\n\n" + "\n".join(commands))

