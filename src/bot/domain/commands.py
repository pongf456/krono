import asyncio
from telegram import Bot, Update
from telegram.ext import ContextTypes
from src.bot.domain.types import Client, Database


class CommandHandler:
    def __init__(self, bot: Bot, database: Database) -> None:
        self.bot = bot
        self.database = database

    async def start(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        response = (
            "<b>👋 ¡Hola! Soy Watchtower Bot!</b> \n"
            "Mi misión es enviarte alertas de <i>Infierno</i> prueba /enable para activar las notificaciones y /disable para desactivarlas"
        )
        if not update.message:
            return
        await update.message.reply_html(response)

    async def enable(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        response = (
            "<b>🔔 Notificaciones Activadas 🔔</b> \n"
            "🤖 El bot <b>Watchtower</b> ha iniciado su vigilancia. \n"
            "\n Alertas de <b>Infierno</b> (de cada hora). \n"
            "Estás recibiendo: \n"
            "Avisos de <b>Reunión</b> de Gremio. \n"
            "Para silenciarme, usa el comando \n /disable \n"
        )
        if not update.message:
            return
        in_db = await self.database.get(update.message.chat_id)
        if not in_db:
            await self.database.store(
                Client(
                    {
                        "name": update.message.chat.first_name or "Usuario",
                        "identifier": update.message.chat_id,
                    }
                )
            )
        await update.message.reply_html(response)

    async def disable(self, update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        response = (
            "<b>🔕 Notificaciones Desactivadas 🔕</b> \n"
            "🤖 El bot <b>Watchtower</b> ha detenido su vigilancia. \n"
            "Para volver a activarlas, usa el comando /enable."
        )
        if not update.message:
            return
        in_db = await self.database.get(update.message.chat_id)
        if in_db:
            await self.database.delete(update.message.chat_id)
        await update.message.reply_html(response)

    async def notify(self, message: str):
        tasks = []
        clients = await self.database.all()
        for client in clients:
            try:
                task = self.bot.sendMessage(
                    client["identifier"],
                    message,
                    parse_mode="MarkdownV2",
                )
                tasks.append(task)
            except:
                print("Ocurrió un error al enviar el mensaje")
        await asyncio.gather(*tasks)
