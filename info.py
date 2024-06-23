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
VERIFIED_CHANNEL = int(environ.get('VERIFIED_CHANNEL', 0))
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
MYSTORE = is_enabled(environ.get('MYSTORE', "False"), False)
MAIN_CHANNEL = int(environ.get('MAIN_CHANNEL', 0))
IS_VERIFY = is_enabled((environ.get('IS_VERIFY', 'False')), False)
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/c/1845700490/3")
SHORTLINK_URL = environ.get('SHORTLINK_URL', "runurl.in") # runurlx
SHORTLINK_API = environ.get('SHORTLINK_API', "868966540ff18e4c2ad2e73343cb2f33181acedb")

VERIFY2_URL = environ.get('VERIFY2_URL', "runurl.in") # Frist 
VERIFY2_API = environ.get('VERIFY2_API', "5ed6df09ca6970fb5809dd7b4388b19bc12e9bca")

VERIFY3_URL = environ.get('VERIFY3_URL', "runurl.in") # Third 
VERIFY3_API = environ.get('VERIFY3_API', "4333efb61c180fb738724bfbe54427ba1b666169")

VERIFY4_URL = environ.get('VERIFY4_URL', "runurl.in") # Fourth
VERIFY4_API = environ.get('VERIFY4_API', "d45daa443ecff47b5a4ebae3c803ee3da53a96f4")

VERIFY5_URL = environ.get('VERIFY5_URL', "kingurl.in") # Ongoing 
VERIFY5_API = environ.get('VERIFY5_API', "d5be075758edd71808de5e98b339af720e5eabce")

VERIFY6_URL = environ.get('VERIFY6_URL', "kingurl.in")
VERIFY6_API = environ.get('VERIFY6_API', "c2150e28189cefefd05f8a9c5c5770cc462033e3")

VERIFY7_URL = environ.get('VERIFY7_URL', "vipurl.in") # Frist 
VERIFY7_API = environ.get('VERIFY7_API', "ba4c12b96125e2cc04402e2a9125a8559f27b3fc")

VERIFY8_URL = environ.get('VERIFY8_URL', "vipurl.in") # Second 
VERIFY8_API = environ.get('VERIFY8_API', "dab3cb1c6b806d8ac96c0635793f12ad87cce803")

VERIFY9_URL = environ.get('VERIFY9_URL', "ziplinker.net") # oneman
VERIFY9_API = environ.get('VERIFY9_API', "603c7a037b8bf4d5a9d2eaa43df6b84783da7aa6")

VERIFY10_URL = environ.get('VERIFY10_URL', "ziplinker.net") # adventure 
VERIFY10_API = environ.get('VERIFY10_API', "12f1784cd5831936c8e4c6f5e414a2f31a22eb2f")
