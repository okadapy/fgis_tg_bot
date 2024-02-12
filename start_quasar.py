import asyncio
from aiogram import Bot, Dispatcher
from app.quasar import router as quasar_router
import config

quasar = Dispatcher()
quasar_bot = Bot(config.TG_API_KEY_2)
quasar.include_router(quasar_router)


async def main():
    await quasar.start_polling(quasar_bot)


asyncio.run(main())
