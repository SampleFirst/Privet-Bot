from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
import arial.ttf

# Function to create an image with text
def create_image_with_text(text):
    img = Image.new('RGB', (500, 300), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 20)
    text_width, text_height = draw.textsize(text, font=font)
    position = ((img.width - text_width) // 2, (img.height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)
    file_path = "/tmp/text_image.png"
    img.save(file_path)
    return file_path

@Client.on_message(filters.command("generate_image") & filters.private)
def generate_image(client, message):
    text = message.text.split(" ", 1)[1]
    image_path = create_image_with_text(text)
    client.send_photo(chat_id=message.chat.id, photo=image_path)
