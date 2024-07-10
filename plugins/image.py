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

# Function to generate a pricing plan image
def create_pricing_image(plan_name, price, features):
    img = Image.new('RGB', (500, 700), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Absolute path to your font file
    font_path = str(Path(__file__).parent / "arial.ttf")
    
    # Ensure the font file exists
    if not Path(font_path).exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")
    
    font = ImageFont.truetype(font_path, 20)
    title_font = ImageFont.truetype(font_path, 30)
    
    draw.text((20, 20), plan_name, fill=(0, 0, 0), font=title_font)
    draw.text((20, 70), f"Price: {price}", fill=(0, 0, 0), font=title_font)
    
    y_text = 130
    for feature in features:
        draw.text((20, y_text), f"- {feature}", fill=(0, 0, 0), font=font)
        y_text += 30
    
    file_path = f"/tmp/{plan_name}_pricing.png"
    img.save(file_path)
    return file_path

@Client.on_message(filters.command("image") & filters.private)
async def generate_image(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        image_path = create_image_with_text(text)
        await message.reply_photo(
            photo=image_path,
            caption="Text to Image Generated Successfully",
            quote=True
        )
    except IndexError:
        await message.reply_text(
            text="Please provide text to generate the image."
        )
    except Exception as e:
        await message.reply_text(
            text=f"An error occurred: {e}"
        )

@Client.on_message(filters.command("pricing") & filters.private)
async def generate_pricing_image(client, message):
    try:
        _, plan_name, price, *features = message.text.split("\n")
        image_path = create_pricing_image(plan_name, price, features)
        await message.reply_photo(
            photo=image_path,
            caption="Pricing Plan Image Generated Successfully",
            quote=True
        )
    except ValueError:
        await message.reply_text(
            text="Please provide the pricing plan details in the format: /pricing\nPlan Name\nPrice\nFeature 1\nFeature 2\n..."
        )
    except Exception as e:
        await message.reply_text(
            text=f"An error occurred: {e}"
        )

