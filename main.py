import asyncio

from aiogram import Bot, Dispatcher

from dialogs import routers
from config import Config


async def main():
    config = Config()
    dp = Dispatcher()
    bot = Bot(config.BOT_TOKEN)

    dp.include_routers(*routers)

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
