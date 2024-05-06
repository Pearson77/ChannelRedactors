import csv
import datetime

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

from config import *

client = TelegramClient('session_name', api_id, api_hash)
client.connect()
# Авторизация пользователя
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Введите код из SMS: '))


def get_messages_by_date(dt: datetime.datetime, channel_id: int):
    all_messages = []
    total_count_limit = 0
    total_messages = 0
    offset_id = 0
    while True:
        history = client(GetHistoryRequest(
            peer=channel_id,
            offset_id=offset_id,
            offset_date=dt,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            dict_message = message.to_dict()

            if dict_message.get('action'):
                continue

            light_message_obj = {
                "id": dict_message.get('id'),
                "views": dict_message.get('views'),
                "forwards": dict_message.get('forwards'),
            }
            all_messages.append(light_message_obj)

        offset_id = messages[len(messages) - 1].id
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break
    return all_messages


def get_posts_ids(all_messages) -> list[int]:
    posts_ids = []
    for message in all_messages:
        post_id = message.get('id')
        posts_ids.append(post_id)
    return posts_ids


def exclude_old_posts(posts_before_today, posts_before_week):
    now_posts_ids: list[int] = get_posts_ids(posts_before_today)
    for i in range(len(posts_before_week)):
        post = posts_before_week[i]
        post_id = post.get('id')
        if post_id and post_id in now_posts_ids:
            del posts_before_today['id']
    return posts_before_today


def get_last_week_messages(channel_id):
    """
        algorithm:
        s1 = get posts before last week
        s2 = get posts before today
        last_week_posts = s2 exclude s1

    """
    today = datetime.date.today()  # get today
    week_ago = datetime.date.today() - datetime.timedelta(days=today.weekday() + 7)  # get last week start
    posts_before_week = get_messages_by_date(week_ago, channel_id)  # s1
    posts_before_today = get_messages_by_date(today, channel_id)  # s2
    # excluding
    new_posts = exclude_old_posts(posts_before_today, posts_before_week)
    return new_posts


def summarize_stat(all_messages: list[dict]) -> dict[str, int]:
    week_forwards = 0
    week_views = 0
    for light_message in all_messages:
        week_views += light_message['views']
        week_forwards += light_message['forwards']
    return {'views': week_views, 'forwards': week_forwards}


def scrap_channel_list(channels: list[int]) -> dict[int, dict[str, int]]:
    telegram_stat = []
    for channel_id in channels:
        channel_stat_info = {}
        messages = get_last_week_messages(channel_id)
        channel_stat = summarize_stat(messages)
        channel_stat_info['id'] = channel_id
        channel_stat_info['stat'] = channel_stat
        telegram_stat.append(channel_stat_info)
    return telegram_stat


def main():
    lst = [-1002080144780]
    print(scrap_channel_list(lst))


if __name__ == '__main__':
    main()
