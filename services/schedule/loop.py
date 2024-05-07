import asyncio
import multiprocessing
import time

from models.services import get_users_list
from services.schedule.schedule import check_user


async def function():
    try:
        users_list = await get_users_list()
        for user in users_list:
            await check_user(user)

    except:
        pass


async def loop():
    while True:
        try:
            await function()
            await asyncio.sleep(5)
        except:
            pass


def loop_starter():
    asyncio.run(loop())


async def starter():
    multiprocessing.Process(target=loop_starter).start()
