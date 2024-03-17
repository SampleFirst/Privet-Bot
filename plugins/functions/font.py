from pyrogram import Client, filters
from pyrogram.types import Message

# Function to convert text to capital font style
def convert_to_capital_font(text):
    capital_font = {
        'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ', 'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ',
        'k': 'ᴋ', 'l': 'ʟ', 'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'Q', 'r': 'ʀ', 's': 'ꜱ', 't': 'ᴛ',
        'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x', 'y': 'ʏ', 'z': 'ᴢ'
    }
    converted_text = ''.join(capital_font.get(char.lower(), char) for char in text)
    return converted_text


# Command to handle incoming messages
@Client.on_message(filters.command("font"))
def capital_font(client, message):
    text_to_convert = ' '.join(message.command[1:])
    converted_text = convert_to_capital_font(text_to_convert)
    message.reply(`converted_text`)

