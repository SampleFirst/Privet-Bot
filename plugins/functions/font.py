from pyrogram import Client, filters


@Client.on_message(filters.command("font") & filters.private)
async def change_font(client, message):
    if len(message.command) == 2:
        text = message.text.split(maxsplit=1)[1]
        converted_text = ""
        font_alphabet = {
            'a': 'ᴀ', 'b': 'ʙ', 'c': 'ᴄ', 'd': 'ᴅ', 'e': 'ᴇ', 'f': 'ꜰ',
            'g': 'ɢ', 'h': 'ʜ', 'i': 'ɪ', 'j': 'ᴊ', 'k': 'ᴋ', 'l': 'ʟ',
            'm': 'ᴍ', 'n': 'ɴ', 'o': 'ᴏ', 'p': 'ᴘ', 'q': 'ǫ', 'r': 'ʀ',
            's': 'ꜱ', 't': 'ᴛ', 'u': 'ᴜ', 'v': 'ᴠ', 'w': 'ᴡ', 'x': 'x',
            'y': 'ʏ', 'z': 'ᴢ'
        }
        for char in text.lower():
            if char in font_alphabet:
                converted_text += font_alphabet[char]
            else:
                converted_text += char
        await message.reply(converted_text)
        
