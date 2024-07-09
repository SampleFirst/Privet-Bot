from pyrogram import Client, filters
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

# Function to create an image with text, wrapping and splitting into multiple images if necessary
def create_images_with_text(text, max_width=500, max_height=300, padding=20, font_size=20):
    # Setup
    font_path = str(Path(__file__).parent / "arial.ttf")
    if not Path(font_path).exists():
        raise FileNotFoundError(f"Font file not found: {font_path}")
    font = ImageFont.truetype(font_path, font_size)

    lines = []
    words = text.split()
    current_line = words[0]

    for word in words[1:]:
        test_line = f"{current_line} {word}"
        if font.getsize(test_line)[0] <= max_width - 2 * padding:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    images = []
    current_image_lines = []

    for line in lines:
        if (len(current_image_lines) + 1) * (font_size + padding) > max_height - 2 * padding:
            img = create_image(current_image_lines, max_width, max_height, padding, font)
            images.append(img)
            current_image_lines = []
        current_image_lines.append(line)

    if current_image_lines:
        img = create_image(current_image_lines, max_width, max_height, padding, font)
        images.append(img)

    file_paths = []
    for i, img in enumerate(images):
        file_path = f"/tmp/text_image_{i}.png"
        img.save(file_path)
        file_paths.append(file_path)

    return file_paths

def create_image(lines, max_width, max_height, padding, font):
    img = Image.new('RGB', (max_width, max_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    y_text = padding
    for line in lines:
        width, height = draw.textsize(line, font=font)
        draw.text(((max_width - width) // 2, y_text), line, font=font, fill=(0, 0, 0))
        y_text += height + padding

    return img

@Client.on_message(filters.command("image") & filters.private)
def generate_image(client, message):
    try:
        text = message.text.split(" ", 1)[1]
        image_paths = create_images_with_text(text)
        for image_path in image_paths:
            client.send_photo(chat_id=message.chat.id, photo=image_path)
    except IndexError:
        message.reply_text("Please provide text to generate the image.")
    except Exception as e:
        message.reply_text(f"An error occurred: {e}")

