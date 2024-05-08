from aiogram import Bot

from datetime import date, datetime, timedelta

from models.services import create_user, read_user, new_user_act, get_user_channels
from models.models import get_session
from config import Config

config = Config()
bot = Bot(config.BOT_TOKEN)


async def create_first_task(user_id, channels_ids, schedule_type, start_time, end_time, start_date=None):
    current_date = date.today()
    task_date_time = datetime.today()

    if schedule_type == "5&2":
        if current_date.weekday() < 5:
            target_date = current_date + timedelta(days=0)
        else:
            days_count = 7 - current_date.weekday() + 1
            target_date = current_date + timedelta(days=days_count)
        task_date_time = datetime.combine(target_date, start_time.time())

    if schedule_type == "2&5":
        if current_date.weekday() == 6:
            target_date = current_date + timedelta(days=1)
        else:
            days_count = 6 - current_date.weekday()
            target_date = current_date + timedelta(days=days_count)
        task_date_time = datetime.combine(target_date, start_time.time())

    if schedule_type == "2&2":
        task_date_time = datetime.combine(start_date, start_time.time())

    return await create_user(
        get_session(), user_id, channels_ids, schedule_type, task_date_time, start_time, end_time, "1"
    )


async def set_next_task(user_id):
    user = await read_user(get_session(), user_id)
    task_date_time = datetime.today()
    current_date = date.today()

    task = user["next_act_type"]
    next_ = "del" if task == "add" else "add"
    if next_ == "del":
        days_ = "2" if user["move_type"] == "1" else "1"
    else:
        days_ = user["move_type"]

    if task == "del":
        if user["schedule_type"] == "5&2":
            if current_date.weekday() < 5:
                target_date = current_date + timedelta(days=1)
            else:
                days_count = 7 - current_date.weekday() + 1
                target_date = current_date + timedelta(days=days_count)
            task_date_time = datetime.combine(target_date, user["start_time"].time())

        if user["schedule_type"] == "2&5":
            if current_date.weekday() == 6:
                target_date = current_date + timedelta(days=1)
            else:
                days_count = 6 - current_date.weekday()
                target_date = current_date + timedelta(days=days_count)
            task_date_time = datetime.combine(target_date, user["start_time"].time())

        if user["schedule_type"] == "2&2":
            target_date = current_date + timedelta(days=int(user["move_type"]))
            task_date_time = datetime.combine(target_date, user["start_time"].time())

    else:
        task_date_time = datetime.combine(current_date, user["end_time"].time())

    return await new_user_act(get_session(), user_id, next_, task_date_time, days_)


async def check_user(user_id):
    user = await read_user(get_session(), user_id)
    if user["next_act_time"] > datetime.now():
        return

    current_task = user["next_act_type"]
    await set_next_task(user_id)
    channels = await get_user_channels(user_id)

    if current_task == "add":
        for channel in channels:
            await bot.promote_chat_member(
                user_id=user_id,
                chat_id=channel.channel_id,
                can_post_messages=True,
                request_timeout=10,
            )
    else:
        for channel in channels:
            await bot.promote_chat_member(
                user_id=user_id,
                chat_id=channel.channel_id,
                is_anonymous=False,
                can_manage_chat=False,
                can_delete_messages=False,
                can_manage_video_chats=False,
                can_restrict_members=False,
                can_promote_members=False,
                can_change_info=False,
                can_invite_users=False,
                can_post_stories=False,
                can_edit_stories=False,
                can_delete_stories=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_pin_messages=False,
                can_manage_topics=False,
                request_timeout=10,
            )
