import asyncio
import time
from src.application.types import Client
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import pytz

VENEZUELA_TIMEZONE = pytz.timezone('America/Caracas')
class Scheduler:
    def __init__(self, some_client: Client):
        self.client = some_client
        self._running = False
        self.scheduler = AsyncIOScheduler(timezone=VENEZUELA_TIMEZONE) 

    def setup_jobs(self):
        self.scheduler.add_job(
            self.client.pre_hell_finished, 
            'cron', 
            minute='50'
        )
        self.scheduler.add_job( self.client.hell_finished, 'cron', minute='55')
        self.scheduler.add_job(self.client.pre_hell_started, 'cron', minute='55')
        self.scheduler.add_job(self.client.hell_started, 'cron', minute='00')

    async def start(self):
        self.setup_jobs()
        print("Started scheduler task.")
        self.scheduler.start()
        self._running = True
        while self._running:
            await asyncio.sleep(1)