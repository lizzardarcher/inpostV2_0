import asyncio
import random
import string
import sys
from time import sleep
import datetime
import json
import traceback
import logging
import re
from pyrogram import Client, compose, idle, filters
from pyrogram.handlers import MessageHandler
import os
import django
from pyrogram.enums import ParseMode

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import Account, Bot, TGAdmin, Chat, GeneralSettings, \
    Message, MasterAccount, ChatMaster, ChannelToSubscribe, AccountLogging
from apps.spamer.models import Client as Tg_client

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=logging.INFO,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ],
)


async def main():
    """ Автоответчик """

    """ Пул сессий """
    apps = [Client(x.session.name.split('/')[-1].split('.')[0]) for x in Account.objects.filter(status=True).order_by('first_name')]

    for app in apps:
        logger.info(f'[{app.name}] [started]')
        @app.on_message(filters.text & filters.private)
        async def answer_(client, message):
            account = Account.objects.filter(session=f'sessions/{client.name}.session').last()
            tg_cli = Tg_client.objects.filter(user_id=message.from_user.id, account=account)
            logger.info(f'[{message.text}] [{account}]')

            """
                * Ответ пользователю
                * Создание объекта клиента
            """
            if not tg_cli:
                text = account.auto_answering_text_ref.text
                if not text:
                    text = GeneralSettings.objects.get(pk=1).general_auto_answering
                await asyncio.sleep(0.1)
                await client.send_message(message.chat.id, text)
                user_id = message.from_user.id
                username = message.from_user.username
                first_name = message.from_user.first_name
                if not username: username = str(first_name)
                last_name = message.from_user.last_name
                Tg_client.objects.create(user_id=user_id, username=username, first_name=first_name, last_name=last_name,
                                         account=account)

    """ Активируем клиенты pyrogram с помощью compose() """
    await compose(apps, False)

if __name__ == '__main__':
    asyncio.run(main())
