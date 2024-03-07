class script(object):
    START_TXT = """Hello {user}!\nWelcome to the Bot."""

    BOTS = """Hey {user},\nChoose a Bot Premium category:"""

    DATABASE = """Hey {user},\nChoose a Database Premium category:"""
    
    SELECT_BOT = """🏷 Bot:- {a}\n
⌾ Expiry Date: {b}
⌾ Expiry Time: {c}
⌾ Validity: {d}\n
💰 Price 99₹ Per Month..."""
    
    SELECT_DB = """🏷 Database:- {a}\n
⌾ Expiry Date: {b}
⌾ Expiry Time: {c}
⌾ Validity: {d}\n
💰 Price 99₹ Per Month..."""

    BUY_BOT = """Payment Details\n
Selected Bot: {bot_name}
Price: 99₹
Validity: 30 Days\n
⌾  My name - Soon...\n
⌾  Phone Pay - UPI - Soon...
⌾  Paytm - UPI - Soon...\n
▣  After Payment Send Screenshot in Bot..."""
    
    BUY_DB = """Payment Details\n
Selected Bot: {db_name}
Price: 99₹
Validity: 30 Days\n
⌾  My name - Soon...\n
⌾  Phone Pay - UPI - Soon...
⌾  Paytm - UPI - Soon...\n
▣  After Payment Send Screenshot in Bot..."""

    LOG_PREDB = """🎉 #new_premium\n
User ID: {a}
Username: @{b}
Now Status: {c}
Price: 99₹
Now Date: {d}
Expire Date: {e}"""

    LOG_PREBOT = """🎉 #new_premium\n
User ID: {a}
Username: @{b}
Now Status: {c}
Price: 99₹
Now Date: {d}
Expire Date: {e}"""

    MOVIES_TEXT = """Here are the details about the Movies Bot premium plan:\n\n- Exclusive movie recommendations\n- High-speed streaming access"""
    
    LINK_TEXT = """Here are the details about the Anime Bot premium plan:\n\n- Curated anime suggestions\n- Early access to new episodes"""
    
    RENAME_TEXT = """Here are the details about the Rename Bot premium plan:\n\n- Unlimited username changes\n- Priority support"""
    
    YT_TEXT = """Here are the details about the Yt & Insta Bot premium plan:\n\n- Video and photo download\n- Ad-free experience"""
    
    MOVIESDB_TEXT = """Here are the details about the Movies Database premium plan:\n\n- Extensive movie collection\n- Advanced search features"""
    
    ANIMEDB_TEXT = """Here are the details about the Anime Database premium plan:\n\n- Comprehensive anime database\n- Personalized recommendations"""
    
    SERIESDB_TEXT = """Here are the details about the TV Show Database premium plan:\n\n- Access to a wide range of TV shows\n- Latest episode updates"""

    BOOKSDB_TEXT = """Here are the details about the TV Show Database premium plan:\n\n- Access to a wide range of TV shows\n- Latest episode updates"""
    
    BUY_BOT_PREMIUM = """Hey {user}\n\nThank To Buy A Premium Access For Bot\nMake Patients Admin Review You Request and Sending Confirmation Message soon.."""

    BUY_DB_PREMIUM = """Hey {user}\n\nThank To Buy A Premium Access For Database\nMake Patients Admin Review You Request and Sending Confirmation Message soon.."""

    CONSTRUCTION = """Hey {user}\nThis Feature under construction.\n\nAvailable soon..."""

    HELP_TXT = """<b>Hey {}
Here Is The Help For My Commands.</b>"""

    ABOUT_TXT = """<b>✯ My Name: {}
✯ Creator: <a href='https://t.me/iPepkornBots'>iPepkorn Bots</a>
✯ Library: <a href='https://docs.pyrogram.org/'>Pyrogram</a>
✯ Language: <a href='https://www.python.org/download/releases/3.0/'>Python 3</a>
✯ Database: <a href='https://www.mongodb.com/'>MongoDB</a>
✯ Bot Server: <a href='https://app.koyeb.com/'>Koyeb</a>
✯ Build Status: v1.1.1 [Stable]</b>"""

    STATUS_TXT = """<b>★ Total Files: <code>{}</code>
★ Total Users: <code>{}</code>
★ Total Chats: <code>{}</code>
★ Used Storage: <code>{}</code>
★ Free Storage: <code>{}</code></b>"""

    LOG_TEXT_P = """👤 #NewUser
<b>᚛› ID: <code>{a}</code>
<b>᚛› Name: {b}
<b>᚛› Username: @{c}
<b>᚛› Total: {d}
<b>᚛› Date: <code>{e}</code>
<b>᚛› Time: <code>{f}</code>
<b>᚛› Today Users: {g}
By @{h}"""

    LOG_TEXT_V = """🆕 #UserVerify
ID: <code>{}</code>
Name: {}
Date: <code>{}</code>
Time: <code>{}</code>"""

    LOG_BOT = """🆕️ #new_bot_attempt\n
ID: <code>{a}</code>
Name: @{b}
Bot Name: {c}
Now Status: {d}
Date: <code>{e}</code>
Time: <code>{f}</code>
Exp Date: <code>{g}</code>
Exp Time: <code>{h}</code>"""

    LOG_DB = """🆕️ #new_db_attempt
ID: <code>{b}</code>
Name: {a}
DB Name: {c}
Now Status: {d}
Date: <code>{e}</code>
Time: <code>{f}</code>
Exp Date: <code>{g}</code>
Exp Time: <code>{h}</code>"""

    
    MELCOW_ENG = """<b>Hello {}, and Welcome to {} Group </b> 🌟"""

    LOGO = """Deported"""
