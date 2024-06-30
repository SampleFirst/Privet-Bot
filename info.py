import re
import time
from os import environ
from Script import script

id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# PyroClient Setup
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
SESSION = environ.get('SESSION', 'Media_search')

# Bot settings
WEBHOOK = bool(environ.get("WEBHOOK", True))  # for web support on/off
PICS = (environ.get('PICS', 'https://graph.org/file/01ddfcb1e8203879a63d7.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg https://graph.org/file/a125497b6b85a1d774394.jpg https://graph.org/file/43d26c54d37f4afb830f7.jpg https://graph.org/file/60c1adffc7cc2015f771c.jpg https://graph.org/file/d7b520240b00b7f083a24.jpg https://graph.org/file/0f336b0402db3f2a20037.jpg https://graph.org/file/39cc4e15cad4519d8e932.jpg https://graph.org/file/d59a1108b1ed1c6c6c144.jpg https://te.legra.ph/file/3a4a79f8d5955e64cbb8e.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg')).split()
UPTIME = time.time()

# Admins, Channels & Users
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None

# MongoDB information
DATABASE_URL = environ.get('DATABASE_URL', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "")

# Other Chats
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/+JZNUbgbjTjExMGU1')
UPDATE_CHANNEL = environ.get('UPDATE_CHANNEL', 'https://t.me/+pXzjJ61z81IyMGFl')
BONUS_CHANNEL = int(environ.get('BONUS_CHANNEL', 0))

# Others
PORT = environ.get("PORT", "8080")
REFER_ON = is_enabled(environ.get('REFER_ON', "False"), False)
DAILY_BONUS = is_enabled(environ.get('DAILY_BONUS', "False"), False)
MYSTORE = is_enabled(environ.get('MYSTORE', "False"), False)
MAIN_CHANNEL = int(environ.get('MAIN_CHANNEL', 0))
IS_VERIFY = is_enabled((environ.get('IS_VERIFY', 'False')), False)
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', "https://t.me/c/1845700490/3")
SHORTLINK_URL = environ.get('SHORTLINK_URL', "runurl.in") # runurlx
SHORTLINK_API = environ.get('SHORTLINK_API', "868966540ff18e4c2ad2e73343cb2f33181acedb")

VERIFY2_URL = environ.get('VERIFY2_URL', "runurl.in") # Frist 12$ 960r
VERIFY2_API = environ.get('VERIFY2_API', "5ed6df09ca6970fb5809dd7b4388b19bc12e9bca")

VERIFY3_URL = environ.get('VERIFY3_URL', "runurl.in") # Third 12$ 960r
VERIFY3_API = environ.get('VERIFY3_API', "4333efb61c180fb738724bfbe54427ba1b666169")

VERIFY4_URL = environ.get('VERIFY4_URL', "runurl.in") # Fourth 12$ 960r
VERIFY4_API = environ.get('VERIFY4_API', "d45daa443ecff47b5a4ebae3c803ee3da53a96f4")

VERIFY5_URL = environ.get('VERIFY5_URL', "kingurl.in") # Ongoing 10$ 800r
VERIFY5_API = environ.get('VERIFY5_API', "d5be075758edd71808de5e98b339af720e5eabce")

VERIFY6_URL = environ.get('VERIFY6_URL', "kingurl.in") # Frists 10$ 800r
VERIFY6_API = environ.get('VERIFY6_API', "ff103ac2249036f5aa5eecd61a734c946bc5019a")

VERIFY7_URL = environ.get('VERIFY7_URL', "vipurl.in") # Frist 7$ 539r or 560r
VERIFY7_API = environ.get('VERIFY7_API', "ba4c12b96125e2cc04402e2a9125a8559f27b3fc")

VERIFY8_URL = environ.get('VERIFY8_URL', "vipurl.in") # Second 7$ 539r or 560r
VERIFY8_API = environ.get('VERIFY8_API', "dab3cb1c6b806d8ac96c0635793f12ad87cce803")

VERIFY9_URL = environ.get('VERIFY9_URL', "ziplinker.net") # oneman 450r
VERIFY9_API = environ.get('VERIFY9_API', "603c7a037b8bf4d5a9d2eaa43df6b84783da7aa6")

VERIFY10_URL = environ.get('VERIFY10_URL', "ziplinker.net") # adventure 450r
VERIFY10_API = environ.get('VERIFY10_API', "12f1784cd5831936c8e4c6f5e414a2f31a22eb2f")
