class script(object):
    START_TEXT = """Hello {user}! Welcome to the Bot.\n
✅ Earn Coins
✅ Buy Subscription\n

/help - information on how to earn coins
/about - View available items in my store
/bonus - send Command and get bonus

Bot Uptime: <code>{now}</code>"""
    
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
1) DRM Downloader Bot (OTT List /ott)
2) OTT Notification Bot (OTT List /nott)
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
💰 Per Refer: 20 Coins
📝 Total Referrals: {total_referrals}\n
Note: Per Join User Through your referral link, when the user watches their first ad, you earn 10 Coins.\n
Share your referral link below:"""

    REFEROFF_TEXT = """Hey {user}!\nReferral program is currently disabled."""
    
    BONUS_TEXT = """Hello {user},\n🎉 Congratulation, you Received {coins} Bonus Coins of the day Try Again next day"""
    
    BONUSOFF_TEXT = """Hey {user}!\nSorry But Your already Received Bonus of the day Coins"""
    
    BONUSFLOOD_TEXT = """Hey Admin\nid: {user_id}\nName: {username}\nTrying Again For Bonus"""
    
    ADS_TEXT = """Hey {user} 💕\n\nComplete This Task And Earn Random Coins."""
    
    EARNCOIN_TEXT = """Congratulations! You've complete the daily coins limit\n
Next Task: <code>{exact_date_time}</code>\n
Left time: <code>{total_time_left}</code>"""

    EARNED_TEXT = """Congratulations! 🎉\nYou have earned {coinz} coins.\n\nGenerate a new ad link: /earn_coins"""
    
    EB_TEXT = """You have Complete All Ad And earned Better coins.\n\nBonus Of the Day: /bonus\n\nCheck Total Earned Coins: /balance"""
    
    MYSTORE_TEXT = """Plans Available Soon...\nEarn Coins Fast 💎\n\nPlease contact Admin for more details."""
    
    BONUSLOG_TEXT = """🎉 New User Claimed Bonus 🎉\n
🆔 User ID = {user}
👁️‍🗨️ Coins = {coins}\n
👮🏻‍♂ Bot = @{bot}"""
    
    STATS_TEXT = """**Bot Stats\n
Total Users: {total_users}
Database Size: {size}
Free Space: {free}**"""
            
    LOG_TEXT_P = """#NewUser
ID - <code>{a}</code>
Name - {b}
Mention - {c}"""
    
    VERIFICATION_TEXT = """🎉 New User Earned Coins 🎉\n
🆔 User ID = {user}
👁️‍🗨️ Coins = {coins}\n
👮🏻‍♂ Bot = @{bot}"""

    RESTART_TXT = """#Restarted

🔄 Bot Restarted!
📅 Date: <code>{a}</code>
⏰ Time: <code>{b}</code>
🌐 Timezone: <code>Asia/Kolkata</code>

#{c}
#Restart_{c}"""
