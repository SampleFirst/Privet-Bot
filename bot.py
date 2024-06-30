import logging
import logging.config
import asyncio

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)

import os
from aiohttp import web
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, PORT
from plugins import web_server
from utils import temp

class Bot(Client):
    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )
        
    async def start(self):
        await super().start()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = me.username
        await self.send_message(chat_id=LOG_CHANNEL, text=(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}."))
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Restarting.......")

app = Bot()
app.run()
