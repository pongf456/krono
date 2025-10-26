import os
from telegram.ext import (
    Application,
    CommandHandler as CM,
)

from src.bot.app.database_sqlite import DatabaseSqlite
from src.bot.domain.commands import CommandHandler
from src.bot.domain.handler import EventHandler


class Bot:
    def __init__(self):
        self.TOKEN = os.environ.get("TELEGRAM_TOKEN")
        if not self.TOKEN:
            raise ValueError("Telegram token not found")
        self.app = Application.builder().token(self.TOKEN).build()
        self.commands = CommandHandler(self.app.bot, DatabaseSqlite())
        self.handler = EventHandler(self.commands.notify)

    async def start(self):
        self.app.add_handlers(
            [
                CM("start", self.commands.start),
                CM("enable", self.commands.enable),
                CM("disable", self.commands.disable),
            ]
        )
        await self.app.initialize()
        if self.app.post_init:
            await self.app.post_init(self.app)
        if self.app.updater:
            await self.app.updater.start_polling()
        await self.app.start()
        print("Started bot...")

    async def stop(self):
        await self.app.stop()
        print("Stopped bot...")
