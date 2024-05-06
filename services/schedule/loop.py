import asyncio
import threading

from models.services import get_users_list
from services.schedule.schedule import check_user


async def function():
    try:
        users_list = await get_users_list()
        for user in users_list:
            await check_user(user)

    except:
        pass


def loop():
    while True:
        try:
            asyncio.run(function())
        except:
            pass


async def starter():
    threading.Thread(target=loop).start()
