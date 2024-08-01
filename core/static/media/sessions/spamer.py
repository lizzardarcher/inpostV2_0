import datetime
import json
import logging
import os
import asyncio
import string
import random
import sys
import traceback
from pathlib import Path
from time import sleep

import pyrogram
from pyrogram import Client

from django.core.files import File
import django
from pyrogram.enums import ParseMode

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import Account, AccountLogging, Message, Chat

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.WARNING,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ],
)

"""
   Спамер асинхронный
   
1. Проходимся по списку аккаунтов, которые (активированы, спам-актив, незаблокированные) 
2. Проходимся по списку спам-чатов
3. Постим сообщения с задержкой
4. Результат в лог
5. Ошибки в лог
6. Если акк забанен акк помечается как заблокированный

"""


def random_string(letter_count, digit_count):
    """
    :param letter_count: letter count
    :param digit_count: digit count
    :return: random string
    """
    str1 = ''.join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
    final_string = ''.join(sam_list)
    return f'\n||ID: {final_string}||'


async def check_if_joined(client, chat_id):
    """Checks if the client is already a member of the specified chat.

    Args:
        client: The Pyrogram client instance.
        chat_id: The chat ID (integer or string) to check.

    Returns:
        True if the client is a member, False otherwise.
    """
    try:
        await client.get_chat_member(chat_id=chat_id, user_id=client.me.id)
        return True  # Member found
    except Exception as e:
        print(f"Error checking membership: {e}")
        return False


async def post_to_chats(acc_id):
    """
    :param acc_id: id of the account
    """

    while True:

        # Рандомная задержка старта спама от 1 до 30 сек.
        # await asyncio.sleep(random.randint(a=1, b=30))

        # Получаем акк по id
        acc = Account.objects.filter(id_account=acc_id)[0]
        logger.info(f'[Activating] [{acc}]')

        # Получаем все активные чаты
        chats = Chat.objects.filter(is_active=True).order_by('?')
        logger.info(f'[List Chats] [{chats}]')

        acc_id = acc.id_account
        session_name = acc.session.name.split('/')[-1].split('.')[0]
        user = acc.user
        logger.info(f'[Account ID] [{acc_id}] [Session name] [{session_name}] [USER] [{user}]')

        try:

            # Активируем клиент
            client = Client(name=session_name)
            logger.info(f'[Client connected] [{client}]')
            await client.start()

            # Проход по группам
            for chat in chats:

                chat_username = chat.username.split('/')[-1]

                # Удаляем предыдущее сообщение, если дозволено
                if chat.is_del_mes_available:
                    try:
                        message = Message.objects.filter(chat=chat.id, account=acc_id, is_deleted=False).last()
                        m_id = message.id
                        message_to_delete = message.message_id
                        await client.delete_messages(chat_username, message_to_delete)
                        Message.objects.filter(id=m_id).update(is_deleted=True)
                    except Exception as e:
                        print(e)

                # Удаляем Emoji, если в чате они запрещены
                if not chat.is_emoji_allowed:
                    import re
                    emoji_pattern = re.compile("["
                                               u"\U0001F600-\U0001F64F"  # emoticons
                                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                               "]+", flags=re.UNICODE)
                    text = emoji_pattern.sub(r'', text)  # no emoji

                # Присоединяемся к чату, если необходимо
                # if await check_if_joined(client, chat_username):
                try:
                    logger.info(f'[Join chat] [{chat_username}] [TRY]')
                    await client.join_chat(chat_id=chat_username)
                    await client.archive_chats(chat_ids=chat_username)
                    logger.info(f'[Join chat] [{chat_username}] [SUCCESS]')
                    await asyncio.sleep(1.5)
                except Exception as e:
                    print(e)
                    await asyncio.sleep(4.1)

                try:
                    # Текст с уникальной сгенерированной строкой в конце
                    text = acc.common_text + random_string(letter_count=6, digit_count=6)

                    # Отправляем сообщение
                    logger.info(f'[Send message] [{text}] [TRY]')
                    res = await client.send_message(chat_id=chat_username, text=text, parse_mode=ParseMode.MARKDOWN)
                    logger.info(f'[Send message] [{chat_username}] [SUCCESS]')
                    jsn = json.loads(str(res))
                    await asyncio.sleep(7.7)

                    # Записываем сообщение в базу
                    account_obj = Account.objects.filter(id_account=jsn['from_user']['id'])[0]
                    chat_obj = Chat.objects.filter(id=chat.id)[0]
                    Message.objects.create(message_id=jsn['id'], account=account_obj,
                                           datetime=datetime.datetime.now(), chat=chat_obj)
                    AccountLogging.objects.create(log_level='Info', account=acc,
                                                  message='MESSAGE SENT',
                                                  datetime=datetime.datetime.now(), chat=chat)
                except Exception as e:
                    print(e)
                    if '401 USER_DEACTIVATED_BAN' in traceback.format_exc():
                        Account.objects.filter(id_account=acc_id).update(status=False)
                        AccountLogging.objects.create(log_level='Fatal', account=acc,
                                                      message='401 USER_DEACTIVATED_BAN',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '400 USER_BANNED_IN_CHANNEL' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='400 USER_BANNED_IN_CHANNEL',
                                                      datetime=datetime.datetime.now(), chat=chat)
                        chat.is_user_banned.add(Account.objects.get(id_account=acc_id))
                    elif '403 CHAT_WRITE_FORBIDDEN' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='403 CHAT_WRITE_FORBIDDEN',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '403 CHAT_SEND_MEDIA_FORBIDDEN' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='403 CHAT_SEND_MEDIA_FORBIDDEN',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '420 SLOWMODE_WAIT_X' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='420 SLOWMODE_WAIT_X',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '403 CHAT_SEND_PLAIN_FORBIDDEN' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='403 CHAT_SEND_PLAIN_FORBIDDEN',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '400 TOPIC_CLOSED' in traceback.format_exc():
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message='400 TOPIC_CLOSED',
                                                      datetime=datetime.datetime.now(), chat=chat)
                    elif '420 FLOOD_WAIT_X' in traceback.format_exc():
                        sec = traceback.format_exc().split('A wait of')[-1].split('seconds')[0]
                        msg = f'Wait {sec} seconds'
                        AccountLogging.objects.create(log_level='Warning', account=acc,
                                                      message=msg,
                                                      datetime=datetime.datetime.now(), chat=chat)
                    else:
                        AccountLogging.objects.create(log_level='Fatal', account=acc,
                                                      message=f'UNKNOWN: {traceback.format_exc()}',
                                                      datetime=datetime.datetime.now(), chat=chat)
            await asyncio.sleep(0.01)
            await client.stop()
            await asyncio.sleep(acc.delay * 60)
        except Exception as e:
            print(e)
            print(traceback.format_exc())


if __name__ == '__main__':

    # Список аккаунтов по фильтру -> [активирован] [незабанен] [спам активен]
    accounts = Account.objects.filter(account_enabled=True, status=True, is_spam_active=True)
    logger.info(f'[Initial accounts][{accounts}]')

    loop = asyncio.get_event_loop()

    for account in accounts:
        """
        Новый аккаунт в отдельный поток выполнения
        """
        loop.create_task(post_to_chats(account.id_account))

    loop.run_forever()
