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
UPI_PIC = environ.get('UPI_PIC', 'https://telegra.ph/file/7e56d907542396289fee4.jpg')

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

PREMIUM_LOGS = int(environ.get('PREMIUM_LOGS', 0))
PAYMENT_CHAT = int(environ.get('PAYMENT_CHAT', 0))

# Database mchannels
MOVIES_DB = [int(mch) if id_pattern.search(mch) else mch for mch in environ.get('MOVIES_DB', '0').split()]
ANIME_DB = [int(ach) if id_pattern.search(ach) else ach for ach in environ.get('ANIME_DB', '0').split()]
SERIES_DB = [int(sch) if id_pattern.search(sch) else sch for sch in environ.get('SERIES_DB', '0').split()]
AUDIOBOOK_DB = [int(bch) if id_pattern.search(bch) else bch for bch in environ.get('AUDIOBOOK_DB', '0').split()]

PORT = environ.get("PORT", "8080")

