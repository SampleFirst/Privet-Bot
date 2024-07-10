from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import asyncio

# Function to create an image with text
def create_image_with_text(text):
    img = Image.new('RGB', (500, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Absolute path to your font file
    font_path = str(Path(__file__).parent / "arial.ttf")
    
    # Ensure the font file exists
    if not Path(font_path).exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    font = ImageFont.truetype(font_path, 20)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)
    
    file_path = "/tmp/text_image.png"
    img.save(file_path)
    return file_path

@Client.on_message(filters.command("image") & filters.private)
async def generate_image(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        image_path = create_image_with_text(text)
        await message.reply_photo(
            photo=image_path,
            caption="Text to Image Generate Successfully",
            quote=True
        )
    except IndexError:
        message.reply_text("Please provide text to generate the image.")
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")
