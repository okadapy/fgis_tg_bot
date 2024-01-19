import asyncio
from aiogram import Bot, Dispatcher
from app.database.requests import create_tables
from app.handlers import router as user_handlers_router
import config

bot = Bot(config.TG_API_KEY)
dp = Dispatcher()
dp.include_routers(user_handlers_router)


async def main():
    await create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
