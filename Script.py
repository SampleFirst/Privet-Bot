class script(object):
    START_TXT = """Hello {user}!\nWelcome to the Bot.\n
Watch Ads and Earn\n
Earn 20 Coins per Ad\n
Once you reach the threshold, you can buy items from my store.\n
/help - For help and information on how to earn coins\n
/about - View available items in my store"""
    
    HELP_TXT = """Hello {user}!\nHere's a step-by-step guide to using the bot:\n
1) Send the /start command to the bot.
2) Click the "Earn Coins" button or send /earn_coins.
3) Watch ad and get 20 Coins 
3) You can watch up to 20 ads per day.
4) Earn 20 coins for each ad you watch.
5) Check your total coins by clicking the "Balance 💰" button or sending the "balance" command.
6) Once you've collected enough coins, check the available items in the store by clicking the "My Store" button or sending the "mystore" command.

Note: After watching 20 ads in a day, you will be eligible for a random bonus by clicking the "Bonus" button or sending the "bonus" command.
Note: Purchases are only available on Saturdays."""

    ABOUT_TXT = """Hello {user}!\nI am the MyStore Bot. Here, you can buy subscriptions to different bots:\n
1) DRM Downloader Bot (Limited OTT)
2) OTT Notification Bot (Limited OTT)
3) 4GB Rename Bot
4) 4GB Uploader Bot

For any queries, ask @xyz."""

    LOG_TEXT_P = """#NewUser
ID - <code>{a}</code>
Name - {b}
Mention - {c}
"""
