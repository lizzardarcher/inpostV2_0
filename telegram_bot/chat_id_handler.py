import logging
import sys
import traceback
from time import sleep
import json

import requests

from database import (get_all, DB_CONNECTION, update, GET_BOT_TOKEN, GET_CHAT_REF_TITLE, UPDATE_CHAT_ID)


logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ],
)

def update_chat_id():
    chats = get_all(DB_CONNECTION, GET_CHAT_REF_TITLE)
    bot_tokens = get_all(DB_CONNECTION, GET_BOT_TOKEN)
    try:
        for chat in chats:
            logger.info(chat)
            sleep(4)
            chat_ref = chat[0]
            chat_title = chat[1]
            for token in bot_tokens:
                r = requests.get(f'https://api.telegram.org/bot{token[0]}/getUpdates').text
                data = json.loads(r)
                if data['ok'] == True:
                    for _data in data['result']:
                        try:
                            chat_id = _data['my_chat_member']['chat']['id']
                            chat_t = _data['my_chat_member']['chat']['title']
                            if chat_title == chat_t:
                                logger.info(f"[{chat_title}] [{chat_t}]")
                                logger.info('SUPER!!!')
                                update(DB_CONNECTION, UPDATE_CHAT_ID, (chat_id, chat_title))
                        except:
                            pass
                else:
                    logger.info(data)
    except:
        logger.info(traceback.format_exc())


while True:
    try:
        logger.info('Pending ...')
        update_chat_id()

        sleep(10)
    except:
        sleep(10)
