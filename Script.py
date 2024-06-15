class script(object):
    START_TEXT = """Hello {user}!\nWelcome to the Bot.\n
Watch Ads and Earn. Earn 20 Coins per Ad\n
Once you reach the threshold, you can buy items from my store.\n
/help - information on how to earn coins\n
/about - View available items in my store
/bonus - send Command and get bonus"""
    
    HELP_TEXT = """Hello {user}!\nHere's a step-by-step guide to using the bot:\n
1) Send the /start command to the bot.
2) Click the <code>Earn Coins 🪙</code> button or send /earn_coins.
3) Watch ad and get 20 Coins 
3) You can watch up to 20 ads per day.
4) Earn 20 coins for each ad you watch.
5) Check your total coins by clicking the <code>Balance 💰</code> button or sending the /balance command.
6) Once you've collected enough coins, check the available items in the store by clicking the <code>My Store 🛒</code> button or sending the /mystore command.

Note: After watching 20 ads in a day, you will be eligible for a random bonus by clicking the <code>Bonus 🎁</code> button or sending the /bonus command.
Note: Purchases are only available on Saturdays."""

    ABOUT_TEXT = """Hello {user}!\nI am the MyStore Bot. Here, you can buy subscriptions to different bots:\n
1) DRM Downloader Bot (Limited OTT)
2) OTT Notification Bot (Limited OTT)
3) 4GB Rename Bot
4) 4GB Uploader Bot

For any queries, ask @xyz."""

    FORCESUB_TEXT = """**Hello {user},
Due to overload only my channel subscribers can use me.\n
Please join my channel and then start me again!...**"""

    BALANCE_TEXT = """🆔 User: {username}\n
🔗 Refer Earn: {refer}\n
💳 Coins: {balance}"""
    
    REFER_TEXT = """Hello {user},
💰 Per Refer: 10 Coins
📝 Total Referrals: {total_referrals}\n
Note: Per Join User Through your referral link, when the user watches their first ad, you earn 10 Coins.\n
"Share your referral link below:"""

    REFEROFF_TEXT = """Hey {user}! Referral program is currently disabled."""
    
    BONUS_TEXT = """Hello {user},\nCongratulation, 🎉 you Received 10 Coins"""
    
    BONUSOFF_TEXT = """Hey {user}!\nSorry But Your already Received Bonus of the day 10 Coins"""
    
    BONUSFLOOD_TEXT = """Hey Admin\nid: {user_id}\nName: {username} Try Again For Bonus"""
    
    EARNING_TEXT = """"Hey {user} 💕\n\nComplete This Ad And Earn 10 Coins."""
    
    EARNCOIN_TEXT = """"Congratulations! You've reached the daily coins limit set by our coins management system, Please try again after 24 hours."""
    
    WITHDRAW_TEXT = """📤 You can withdraw your balance once you reach the minimum threshold. Please contact support for more details."""
    
    STATS_TEXT = """Bot Stats\n
Total Users: {total_users}\n"
Database Size: {size}\n"
Free Space: {free}"""
            
    LOG_TEXT_P = """#NewUser
ID - <code>{a}</code>
Name - {b}
Mention - {c}
"""
