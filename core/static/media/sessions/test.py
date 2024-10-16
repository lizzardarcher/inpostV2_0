import datetime
import json
import logging
import os
import string
import random
import traceback
import asyncio
import sqlite3
import sys
from pyrogram import Client, compose, filters, idle
from pyrogram.enums import ParseMode
import django
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from apps.spamer.models import GeneralSettings
from apps.spamer.models import Client as Tg_client
from apps.spamer.models import Account, AccountLogging, Message, Chat

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ],
)

import signal

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    self.kill_now = True


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


async def post_to_chats(client):
    """
    :param acc_id: id of the account
    """

    while True:

        # Получаем акк по id
        acc = Account.objects.filter(session=f'sessions/{client.name}.session').last()
        logger.info(f'[Activating] [{acc}]')

        # Получаем все активные чаты
        chats = Chat.objects.filter(is_active=True)
        logger.info(f'[List Chats] [{chats}]')

        acc_id = acc.id_account
        # session_name = acc.session_for_chat.split('/')[-1].split('.')[0]
        session_name = acc.session.name.split('/')[-1].split('.')[0]
        user = acc.user
        logger.info(f'[Account ID] [{acc_id}] [Session name] [{session_name}] [USER] [{user}]')

        # Текст с уникальной сгенерированной строкой в конце
        text = acc.common_text_ref.text + random_string(letter_count=6, digit_count=6)
        try:

            # Активируем клиент
            client = Client(name=session_name)
            logger.info(f'[Client connected] [{client}]')
            await client.start()

            # Проход по группам
            for chat in chats:
                if chat.user == acc.user:
                    # if acc not in chat.is_user_banned:

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
                            logger.error(e)

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
                    try:
                        # joined = await client.get_chat(chat_id=chat_username)
                        # if not isinstance(joined, _chat):
                        logger.info(f'[Join chat] [{chat_username}] [TRY]')
                        await client.join_chat(chat_id=chat_username)
                        await client.archive_chats(chat_ids=chat_username)
                        logger.info(f'[Join chat] [{chat_username}] [SUCCESS]')
                        await asyncio.sleep(1.5)
                        # else:
                        #     logger.info(f'[ALREADY JOINED] [{chat_username}] [SKIPPING]')
                        #     await asyncio.sleep(0.5)

                    except Exception as e:
                        logger.error(e)
                        await asyncio.sleep(4.1)

                    try:

                        # Отправляем сообщение
                        res = await client.send_message(chat_id=chat_username, text=text, parse_mode=ParseMode.MARKDOWN)
                        logger.info(f'[Send message] [{acc}] [{chat_username}] [SUCCESS]')
                        jsn = json.loads(str(res))

                        # Записываем сообщение в базу
                        account_obj = Account.objects.filter(id_account=jsn['from_user']['id'])[0]
                        chat_obj = Chat.objects.filter(id=chat.id)[0]
                        Message.objects.create(message_id=jsn['id'], account=account_obj,
                                               datetime=datetime.datetime.now(), chat=chat_obj)
                        AccountLogging.objects.create(log_level='Info', account=acc, user=user,
                                                      message='MESSAGE SENT',
                                                      datetime=datetime.datetime.now(), chat=chat)
                        await asyncio.sleep(acc.delay_2)

                    except Exception as e:
                        logger.error(e)
                        if '401 USER_DEACTIVATED_BAN' in traceback.format_exc():
                            Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                            AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                          message='401 USER_DEACTIVATED_BAN',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '401 AUTH_KEY_UNREGISTERED' in traceback.format_exc():
                            Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                            AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                          message='401 AUTH_KEY_UNREGISTERED',
                                                          datetime=datetime.datetime.now(), chat=None)

                        elif '400 USER_BANNED_IN_CHANNEL' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='400 USER_BANNED_IN_CHANNEL',
                                                          datetime=datetime.datetime.now(), chat=chat)
                            chat.is_user_banned.add(Account.objects.get(id_account=acc_id))
                        elif '403 CHAT_WRITE_FORBIDDEN' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='403 CHAT_WRITE_FORBIDDEN',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '403 CHAT_SEND_MEDIA_FORBIDDEN' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='403 CHAT_SEND_MEDIA_FORBIDDEN',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '420 SLOWMODE_WAIT_X' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='420 SLOWMODE_WAIT_X',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '403 CHAT_SEND_PLAIN_FORBIDDEN' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='403 CHAT_SEND_PLAIN_FORBIDDEN',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '400 TOPIC_CLOSED' in traceback.format_exc():
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message='400 TOPIC_CLOSED',
                                                          datetime=datetime.datetime.now(), chat=chat)
                        elif '420 FLOOD_WAIT_X' in traceback.format_exc():
                            sec = traceback.format_exc().split('A wait of')[-1].split('seconds')[0]
                            msg = f'Wait {sec} seconds'
                            AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                          message=msg,
                                                          datetime=datetime.datetime.now(), chat=chat)
                        else:
                            AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                          message=f'UNKNOWN: {e}',
                                                          datetime=datetime.datetime.now(), chat=chat)
            await asyncio.sleep(0.01)

            await client.stop()
            await asyncio.sleep(acc.delay * 60)
        except Exception as e:
            logger.error(traceback.format_exc())
            if '401 USER_DEACTIVATED_BAN' in traceback.format_exc():
                Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                              message='401 USER_DEACTIVATED_BAN',
                                              datetime=datetime.datetime.now(), chat=None)
                break
            elif '401 AUTH_KEY_UNREGISTERED' in traceback.format_exc():
                Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                              message='401 AUTH_KEY_UNREGISTERED',
                                              datetime=datetime.datetime.now(), chat=None)
                break
            else:
                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                              message=f'{e}',
                                              datetime=datetime.datetime.now(), chat=None)


async def main():
    """ Автоответчик """

    """ Пул сессий """

    # apps = [Client(x.session.name.split('/')[-1].split('.')[0]) for x in Account.objects.filter(
    #     status=True, is_auto_answering_active=True, session__isnull=False).order_by('first_name')]

    apps = []
    accounts = Account.objects.filter(status=True, is_auto_answering_active=True)
    for account in accounts:
        if account.session:
            apps.append(Client(account.session.name.split('/')[-1].split('.')[0]))

    logger.info(apps)
    if not apps:
        sys.exit(1)

    for app in apps:

        @app.on_message(filters.text & filters.private)
        async def auto_answering_handler(client, message):
            account = Account.objects.filter(session=f'sessions/{client.name}.session').last()
            tg_cli = Tg_client.objects.filter(user_id=message.from_user.id, account=account).last()
            logger.info(f'[{message.text}] [{account}] [{tg_cli}] [NOT AUTOANSWERING]')
            """
                * Ответ пользователю
                * Создание объекта клиента
            """

            logger.info(f'[{message.from_user.id}] [NOT CLIENT] [AUTOANSWERING...]')
            text = account.auto_answering_text_ref.text
            if not text:
                text = GeneralSettings.objects.get(pk=1).general_auto_answering
            await asyncio.sleep(4.1)
            await client.send_message(message.chat.id, text)
            user_id = message.from_user.id
            username = message.from_user.username
            first_name = message.from_user.first_name
            if not username: username = str(first_name)
            last_name = message.from_user.last_name
            Tg_client.objects.create(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                                     account=account)

        @app.on_message(filters.sticker)
        async def post_to_chats(client, message):
            """
            :param acc_id: id of the account
            """
            print(message.sticker.file_id)
            print(message.sticker.file_unique_id)
            print(str(message.sticker.file_unique_id) == 'AgADazMAAoiGyUo')
            if message.sticker.file_unique_id ==         'AgADazMAAoiGyUo':
                killer = GracefulKiller()
                while not killer.kill_now:
                    while True:
                        try:

                            # Получаем акк по id
                            acc = Account.objects.filter(session=f'sessions/{client.name}.session').last()
                            logger.info(f'[Activating] [{acc}]')

                            # Получаем все активные чаты
                            chats = Chat.objects.filter(is_active=True)
                            logger.info(f'[List Chats] [{chats}]')

                            acc_id = acc.id_account
                            # session_name = acc.session_for_chat.split('/')[-1].split('.')[0]
                            session_name = acc.session.name.split('/')[-1].split('.')[0]
                            user = acc.user
                            logger.info(f'[Account ID] [{acc_id}] [Session name] [{session_name}] [USER] [{user}]')

                            # Текст с уникальной сгенерированной строкой в конце
                            text = acc.common_text_ref.text + random_string(letter_count=6, digit_count=6)
                            try:

                                # Активируем клиент
                                # client = Client(name=session_name)
                                logger.info(f'[Client connected] [{client}]')
                                # await client.start()
                                #
                                # Проход по группам
                                for chat in chats:
                                    if chat.user == acc.user:
                                        # if acc not in chat.is_user_banned:

                                        chat_username = chat.username.split('/')[-1]

                                        # Удаляем предыдущее сообщение, если дозволено
                                        if chat.is_del_mes_available:
                                            try:
                                                message = Message.objects.filter(chat=chat.id, account=acc_id,
                                                                                 is_deleted=False).last()
                                                m_id = message.id
                                                message_to_delete = message.message_id
                                                await client.delete_messages(chat_username, message_to_delete)
                                                Message.objects.filter(id=m_id).update(is_deleted=True)
                                            except Exception as e:
                                                logger.error(e)

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
                                        try:
                                            # joined = await client.get_chat(chat_id=chat_username)
                                            # if not isinstance(joined, _chat):
                                            logger.info(f'[Join chat] [{chat_username}] [TRY]')
                                            await client.join_chat(chat_id=chat_username)
                                            await client.archive_chats(chat_ids=chat_username)
                                            logger.info(f'[Join chat] [{chat_username}] [SUCCESS]')
                                            await asyncio.sleep(1.5)
                                            # else:
                                            #     logger.info(f'[ALREADY JOINED] [{chat_username}] [SKIPPING]')
                                            #     await asyncio.sleep(0.5)

                                        except Exception as e:
                                            logger.error(e)
                                            await asyncio.sleep(4.1)

                                        try:

                                            # Отправляем сообщение
                                            res = await client.send_message(chat_id=chat_username, text=text,
                                                                            parse_mode=ParseMode.MARKDOWN)
                                            logger.info(f'[Send message] [{acc}] [{chat_username}] [SUCCESS]')
                                            jsn = json.loads(str(res))

                                            # Записываем сообщение в базу
                                            account_obj = Account.objects.filter(id_account=jsn['from_user']['id'])[0]
                                            chat_obj = Chat.objects.filter(id=chat.id)[0]
                                            Message.objects.create(message_id=jsn['id'], account=account_obj,
                                                                   datetime=datetime.datetime.now(), chat=chat_obj)
                                            AccountLogging.objects.create(log_level='Info', account=acc, user=user,
                                                                          message='MESSAGE SENT',
                                                                          datetime=datetime.datetime.now(), chat=chat)
                                            await asyncio.sleep(acc.delay_2)

                                        except Exception as e:
                                            logger.error(e)
                                            if '401 USER_DEACTIVATED_BAN' in traceback.format_exc():
                                                Account.objects.filter(id_account=acc_id).update(status=False,
                                                                                                 is_change_needed=False)
                                                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                              message='401 USER_DEACTIVATED_BAN',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '401 AUTH_KEY_UNREGISTERED' in traceback.format_exc():
                                                Account.objects.filter(id_account=acc_id).update(status=False,
                                                                                                 is_change_needed=False)
                                                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                              message='401 AUTH_KEY_UNREGISTERED',
                                                                              datetime=datetime.datetime.now(), chat=None)

                                            elif '400 USER_BANNED_IN_CHANNEL' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='400 USER_BANNED_IN_CHANNEL',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                                chat.is_user_banned.add(Account.objects.get(id_account=acc_id))
                                            elif '403 CHAT_WRITE_FORBIDDEN' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='403 CHAT_WRITE_FORBIDDEN',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '403 CHAT_SEND_MEDIA_FORBIDDEN' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='403 CHAT_SEND_MEDIA_FORBIDDEN',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '420 SLOWMODE_WAIT_X' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='420 SLOWMODE_WAIT_X',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '403 CHAT_SEND_PLAIN_FORBIDDEN' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='403 CHAT_SEND_PLAIN_FORBIDDEN',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '400 TOPIC_CLOSED' in traceback.format_exc():
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message='400 TOPIC_CLOSED',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            elif '420 FLOOD_WAIT_X' in traceback.format_exc():
                                                sec = traceback.format_exc().split('A wait of')[-1].split('seconds')[0]
                                                msg = f'Wait {sec} seconds'
                                                AccountLogging.objects.create(log_level='Warning', account=acc, user=user,
                                                                              message=msg,
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                            else:
                                                AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                              message=f'UNKNOWN: {e}',
                                                                              datetime=datetime.datetime.now(), chat=chat)
                                await asyncio.sleep(0.01)

                                # await client.stop()
                                await asyncio.sleep(acc.delay * 60)

                            except Exception as e:
                                logger.error(traceback.format_exc())
                                if '401 USER_DEACTIVATED_BAN' in traceback.format_exc():
                                    Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                                    AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                  message='401 USER_DEACTIVATED_BAN',
                                                                  datetime=datetime.datetime.now(), chat=None)
                                    break
                                elif '401 AUTH_KEY_UNREGISTERED' in traceback.format_exc():
                                    Account.objects.filter(id_account=acc_id).update(status=False, is_change_needed=False)
                                    AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                  message='401 AUTH_KEY_UNREGISTERED',
                                                                  datetime=datetime.datetime.now(), chat=None)
                                    break
                                else:
                                    AccountLogging.objects.create(log_level='Fatal', account=acc, user=user,
                                                                  message=f'{e}',
                                                                  datetime=datetime.datetime.now(), chat=None)
                        except KeyboardInterrupt:
                            break

    # for app in apps:
    #     await app.start()
    #     await app.send_sticker('me', 'CAACAgIAAxkBAAEJOtBnD8vvXfvi4FZb_dPwiGZNJeVHsAACgzIAAgJ5yUqH1l_r7VRqsjYE')
    #     await app.stop()

    await compose(apps)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except sqlite3.OperationalError as e:
        print(e)
    except KeyboardInterrupt:
        sys.exit(0)


