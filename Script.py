class script(object):
    START_TEXT = """Hello {user}! Welcome to the Bot.\n
✅ Watch Ads
✅ Earn Coins
✅ Buy Subscription of Premium Bots\n

/help - information on how to earn coins
/about - View available items in my store
/bonus - send Command and get bonus"""
    
    HELP_TEXT = """Hello {user}!\nHere's a step-by-step guide to using the bot:\n
⭐ Send the /start command to the bot.
⭐ Click the <code>Bonus 🎁</code> button or send /bonus for Daily bonus.
⭐ Click the <code>Earn Coins 🪙</code> button or send /earn_coins.
⭐ Watch ad and get 10 Coins
⭐ You can watch up to 10 ads per day.
⭐ Earn 10 coins for each ad you watch.
⭐ Check your total coins by clicking the <code>Balance 💰</code> button or sending the /balance command.
⭐ Once you've collected enough coins, check the available items in the store by clicking the <code>My Store 🛒</code> button or sending the /mystore command.

Note: After watching 20 ads in a day, you will be eligible for a random bonus by clicking the <code>Bonus 🎁</code> button or sending the /bonus command.
Note: Purchases are only available on Saturdays."""

    ABOUT_TEXT = """Hello {user}!\nI am the MyStore Bot. Here, you can buy subscriptions to different bots:\n
1) DRM Downloader Bot (Limited OTT)
2) OTT Notification Bot (Limited OTT)
3) 4GB Rename Bot
4) 4GB Uploader Bot

Earn 10 Coins per Ad, Once you reach the threshold, you can buy items from my store.

For any queries, ask @xyz."""

    FORCESUB_TEXT = """**Hello {user},
Due to overload only my channel subscribers can use me.\n
Please join my channels and then start me again!...**"""

    BALANCE_TEXT = """🆔 User: {username}\n
🔗 Refer Earn: {refer}\n
💳 Coins: {balance}"""
    
    REFER_TEXT = """Hello {user},\n
💰 Per Refer: 10 Coins
📝 Total Referrals: {total_referrals}\n
Note: Per Join User Through your referral link, when the user watches their first ad, you earn 10 Coins.\n
Share your referral link below:"""

    REFEROFF_TEXT = """Hey {user}!\nReferral program is currently disabled."""
    
    BONUS_TEXT = """Hello {user},\n🎉 Congratulation, you Received 10 Bonus Coins"""
    
    BONUSOFF_TEXT = """Hey {user}!\nSorry But Your already Received Bonus of the day 10 Coins"""
    
    BONUSFLOOD_TEXT = """Hey Admin\nid: {user_id}\nName: {username}\nTrying Again For Bonus"""
    
    ADS_TEXT = """Hey {user} 💕\n\nComplete This Ad And Earn 10 Coins."""
    
    EARNCOIN_TEXT = """Congratulations! You've complete the daily coins limit set by our coins management system, Please try again after 24 hours."""
    
    MYSTORE_TEXT = """📤 You can withdraw your balance once you reach the minimum threshold. Please contact support for more details."""
    
    STATS_TEXT = """**Bot Stats\n
Total Users: {total_users}
Database Size: {size}
Free Space: {free}**"""
            
    LOG_TEXT_P = """#NewUser
ID - <code>{a}</code>
Name - {b}
Mention - {c}"""
