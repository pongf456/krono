from types import CoroutineType
from typing import Any, Callable

from src.application.types import Client



class EventHandler(Client):
    def __init__(self, notifier: Callable[[str], CoroutineType[Any, Any, None]]):
        self.notifier = notifier

    async def hell_started(self):
        await self.notifier(
            """*🔥 Infierno Iniciado\\!* ⏳ A farmear la fase en la próxima hora\\. \\[\\/disable\\]"""
        )

    async def pre_hell_finished(self):
        await self.notifier(
            "*⏱️ ¡Infierno x5m\\!* Última llamada para terminar la fase actual\\. ¡Corre\\! \\[\\/disable\\]"
        )

    async def hell_finished(self):
        await self.notifier(
            "*✅ Infierno Finalizado\\!* 😴 Tómate un respiro y prepárate para el siguiente\\. \\[\\/disable\\]"
        )

    async def pre_hell_started(self):
        await self.notifier(
            "*🚨 Infierno en 5 Minutos\\!* Prepárate para iniciar la nueva fase a la hora en punto\\. \\[\\/disable\\]"
        )
