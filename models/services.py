from sqlalchemy import select, insert, delete, update
from models.models import *


async def create_user(session, user_id, channel_id, schedule_type, task_time, start_time, end_time):
    user = Redactor(
        id=user_id,
        schedule_type=schedule_type,
        next_act_type="add",
        next_act_time=task_time,
        start_time=start_time,
        end_time=end_time,
    )
    session.add(user)
    session.commit()

    for channel in [channel_id]:
        session.add(ChannelAccess(redactor_id=user_id, channel_id=channel))
    session.commit()


async def read_user(session, user_id):
    redactor = session.query(Redactor).filter_by(id=user_id).first()
    return {
        "id": redactor.id,
        "schedule_type": redactor.schedule_type,
        "next_act_type": redactor.next_act_type,
        "next_act_time": redactor.next_act_time,
        "start_time": redactor.start_time,
        "end_time": redactor.end_time,
    }


async def new_user_act(session, user_id, next_act_type, next_act_time):
    redactor = session.query(Redactor).filter_by(id=user_id).first()
    redactor.next_act_type = next_act_type
    redactor.next_act_time = next_act_time
    session.commit()


async def update_user(session, user_id, schedule_type, next_act_type, next_act_time, start_time, end_time):
    redactor = session.query(Redactor).filter_by(id=user_id).first()
    if schedule_type: redactor.schedule_type = schedule_type
    if next_act_type: redactor.next_act_type = next_act_type
    if next_act_time: redactor.next_act_time = next_act_time
    if start_time: redactor.start_time = start_time
    if end_time: redactor.end_time = end_time
    session.commit()


async def delete_user(user_id, session=get_session()) -> bool:
    redactor = session.query(Redactor).filter_by(id=user_id).first()
    if not redactor:
        return False
    session.execute(delete(Redactor).where(Redactor.id == user_id))
    session.commit()

    ...
    return True
