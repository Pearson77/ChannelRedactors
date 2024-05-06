from datetime import date, time, datetime, timedelta
from models.services import create_user, read_user, new_user_act
from models.models import get_session


async def create_first_task(user_id, channel_id, schedule_type, start_time, end_time, start_date=None):
    current_date = date.today()
    task_date_time = datetime.today()

    if schedule_type == "5&2":
        if current_date.weekday() < 5:
            target_date = current_date + timedelta(days=1)
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

    return await create_user(get_session(), user_id, channel_id, schedule_type, task_date_time, start_time, end_time)


async def set_next_task(user_id):
    user = await read_user(get_session(), user_id)
    task_date_time = datetime.today()
    current_date = date.today()

    task = user["next_act_type"]
    next_ = "del" if task == "add" else "add"

    if task == "add":
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
            target_date = current_date + timedelta(days=2)
            task_date_time = datetime.combine(target_date, user["start_time"].time())

    else:
        task_date_time = datetime.combine(current_date, user["end_time"].time())

    return new_user_act(get_session(), user_id, next_, task_date_time)
