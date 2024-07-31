import traceback
from database import (get_all, update_chat_stats, GET_ALL_CHATS, UPDATE_CHAT_STATS, DB_CONNECTION,
                      update, UPDATE_CHAT_INC, UPDATE_CHAT_DEC, GET_CHAT_FOR_STATS, UPDATE_CHAT_SUBS, RESET_INC_DEC)
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep


def update_stats():
    print('HI')
    day_of_week = datetime.now().weekday()
    update_start = str(datetime.today().time().hour)
    if day_of_week == 0:
        dayofweek = 'mon_stat_subs'
    elif day_of_week == 1:
        dayofweek = 'tue_stat_subs'
    elif day_of_week == 2:
        dayofweek = 'wed_stat_subs'
    elif day_of_week == 3:
        dayofweek = 'thu_stat_subs'
    elif day_of_week == 4:
        dayofweek = 'fri_stat_subs'
    elif day_of_week == 5:
        dayofweek = 'sat_stat_subs'
    elif day_of_week == 6:
        dayofweek = 'sun_stat_subs'
    else:
        dayofweek = 'sun_stat_subs'
    chats = get_all(DB_CONNECTION, GET_CHAT_FOR_STATS)

    for chat in chats:
        try:
            chat_type = chat[0]
            url = chat[1]
            chat_id = chat[2]
            total_subs = chat[3]
            neg_subs = chat[4]
            pos_subs = chat[5]
            # print(chat_type, url, chat_id, total_subs, neg_subs, pos_subs)

            if not neg_subs: neg_subs = 0
            if not pos_subs: pos_subs = 0
            r = requests.get(url=url).text
            # print(r)
            soup = BeautifulSoup(r, 'lxml')
            raw_subscribers = soup.find("div", {"class": "tgme_page_extra"}).text
            # print(url)
            # print(raw_subscribers)
            subscribers = ''
            for i in raw_subscribers.split(' '):
                if chat_type == 'Канал':
                    if 'sub' not in i:
                        subscribers += i
                elif chat_type == 'Группа':
                    if 'mem' not in i:
                        subscribers += i
            subscribers = int(subscribers)
            # print(subscribers)

            # update total subscribers
            update(DB_CONNECTION, UPDATE_CHAT_SUBS, (subscribers, chat_id))

            # update daily subscribers
            update_chat_stats(DB_CONNECTION, UPDATE_CHAT_STATS,  dayofweek, (subscribers, chat_id))

            # update difference between negative and positive subs
            diff = total_subs - subscribers
            try:
                if diff <= 0:
                    diff = 0 - diff + pos_subs
                    update(DB_CONNECTION, UPDATE_CHAT_INC, (diff, chat_id))
                    # print(url, 'updated')
                else:
                    diff = diff + neg_subs
                    update(DB_CONNECTION, UPDATE_CHAT_DEC, (diff, chat_id))
                    # print(url, 'updated')
            except:pass

            #  Очистить отписки-подписки
            try:
                if update_start == '0':
                    update(DB_CONNECTION, RESET_INC_DEC, (0, 0, chat_id))
            except:
                print(traceback.format_exc())
        except:
            print(traceback.format_exc())


while True:
    try:
        update_stats()
        sleep(2400)  # 40 minutes
    except:
        sleep(2400)  # 40 minutes
