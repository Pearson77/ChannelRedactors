import asyncio
import threading
import time

from models.services import get_users_list
from services.schedule.schedule import check_user


async def function():
    try:
        users_list = await get_users_list()
        for user in users_list:
            print(user)
            await check_user(user)

    except:
        raise


def loop():
    while True:
        time.sleep(5)
        try:
            asyncio.run(function())
        except:
            raise


async def starter():
    threading.Thread(target=loop).start()
