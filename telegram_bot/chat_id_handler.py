import os
import traceback
from time import sleep
from datetime import datetime
import json

from bs4 import BeautifulSoup
import requests
from telebot import TeleBot
from telebot.types import (InputMediaPhoto,
                           InputMediaVideo,
                           InputMediaAudio,
                           InputMediaDocument,
                           InlineKeyboardMarkup,
                           InlineKeyboardButton,
                           KeyboardButton,
                           ReplyKeyboardMarkup, )

from database import (get_all, update_chat_stats, GET_ALL_CHATS, UPDATE_CHAT_STATS, DB_CONNECTION,
                       update, UPDATE_CHAT_INC, UPDATE_CHAT_DEC, UPDATE_CHAT_SUBS, RESET_INC_DEC,
                       GET_BOT_TOKEN, GET_CHAT_REF_TITLE, UPDATE_CHAT_ID)


def update_chat_id():
    chats = get_all(DB_CONNECTION, GET_CHAT_REF_TITLE)
    bot_tokens = get_all(DB_CONNECTION, GET_BOT_TOKEN)
    try:
        for chat in chats:
            sleep(4)
            chat_ref = chat[0]
            chat_title = chat[1]
            for token in bot_tokens:
                # print(token)
                r = requests.get(f'https://api.telegram.org/bot{token[0]}/getUpdates').text
                data = json.loads(r)
                if data['ok'] == True:
                    # chat_id = data['result'][0]['my_chat_member']['chat']['id']
                    # print(chat_id)
                    for _data in data['result']:
                        try:
                            chat_id = _data['my_chat_member']['chat']['id']
                            chat_t = _data['my_chat_member']['chat']['title']
                            # print(chat_id)
                            # print(chat_t)
                            # print(chat_title, chat_t, flush=True)
                            if chat_title == chat_t:
                                # print('SUPER!!!')
                                update(DB_CONNECTION, UPDATE_CHAT_ID, (chat_id, chat_title))
                        except:
                            pass
                else:
                    print(data)
    except:
        print(traceback.format_exc())

while True:
    try:
        update_chat_id()
        # os.system('apachectl -k graceful')
        sleep(10)
    except:
        sleep(10)
