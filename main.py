import asyncio

from aiogram import F, Bot, Dispatcher

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

    dp.message.filter(
        F.from_user.id == config.ADMIN_ID
    )
    dp.callback_query.filter(
        F.from_user.id == config.ADMIN_ID
    )

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
