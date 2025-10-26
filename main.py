import asyncio
from dotenv import load_dotenv

from src.application.scheduler import Scheduler
from src.bot.main import Bot


load_dotenv()
bot = Bot()
scheduler = Scheduler(bot.handler)

async def main():
    try:
        await asyncio.gather(bot.start(), scheduler.start())
    except asyncio.CancelledError:
        # Si se presiona Ctrl+C, asyncio.gather() lanza CancelledError.
        print('\nKeyboardInterrupt detected. Starting graceful shutdown...')
        # 💡 Llamamos a bot.stop() aquí, DENTRO del bucle asíncrono.
        await bot.stop()
        scheduler._running = False 
        print('success')
        # Opcional: El scheduler ya se detuvo con la cancelación, 
        # pero asegurarse de que la flag esté en False es bueno.

if __name__ == '__main__':
    
    asyncio.run(main())
