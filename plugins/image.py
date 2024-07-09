from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Function to create an image with text
def create_image_with_text(text):
    img_width, img_height = 500, 300
    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Absolute path to your font file
    font_path = str(Path(__file__).parent / "arial.ttf")
    
    # Ensure the font file exists
    if not Path(font_path).exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")

    # Initial font size
    font_size = 20
    font = ImageFont.truetype(font_path, font_size)
    
    # Adjust font size to fit the text within the image
    max_width = img_width - 20
    max_height = img_height - 20
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width and text_height <= max_height:
            break
        font_size -= 1
        if font_size < 10:  # Set a minimum font size
            raise ValueError("Text is too long to fit in the image.")
        font = ImageFont.truetype(font_path, font_size)
    
    position = ((img_width - text_width) // 2, (img_height - text_height) // 2)
    draw.text(position, text, fill=(0, 0, 0), font=font)
    
    file_path = "/tmp/text_image.png"
    img.save(file_path)
    return file_path

@Client.on_message(filters.command("image") & filters.private)
def generate_image(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        image_path = create_image_with_text(text)
        client.send_photo(chat_id=message.chat.id, photo=image_path)
    except IndexError:
        message.reply_text("Please provide text to generate the image.")
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")

