import asyncio

from aiogram import Bot, Dispatcher

from services.schedule.loop import starter
from dialogs import routers
from config import Config


async def on_startup():
    await starter()
    print("Started")


async def main():
    config = Config()
    dp = Dispatcher()
    bot = Bot(config.BOT_TOKEN)

    dp.include_routers(*routers)
    dp.startup.register(on_startup)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
