# info.py
import re
import logging
from os import environ

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

id_pattern = re.compile(r'^.\d+$')


def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
SESSION = environ.get('SESSION', 'Media_search')

# Admin, Channels
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
PICS = environ.get('PICS', 'https://telegra.ph/file/6d98a444198fdac6322c2.jpg').split()

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

PORT = environ.get("PORT", "8080")
REFER_ON = is_enabled(environ.get('REFER_ON', "False"), False)
DAILY_BONUS = is_enabled(environ.get('DAILY_BONUS', "False"), False)
WITHDRAW_BTN = is_enabled(environ.get('WITHDRAW_BTN', "False"), False)
MAIN_CHANNEL = int(environ.get('MAIN_CHANNEL', 0))
IS_VERIFY = is_enabled((environ.get('IS_VERIFY', 'False')), False)
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/c/1845700490/3")
VERIFY2_URL = environ.get('VERIFY2_URL', "clicksfly.com")
VERIFY2_API = environ.get('VERIFY2_API', "c2150e28189cefefd05f8a9c5c5770cc462033e3")
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'clicksfly.com')
SHORTLINK_API = environ.get('SHORTLINK_API', 'c2150e28189cefefd05f8a9c5c5770cc462033e3')

