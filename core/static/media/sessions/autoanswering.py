import asyncio
import sqlite3
import sys
import logging

from django.conf import settings
from pyrogram import Client, compose, filters
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import Account, GeneralSettings
from apps.spamer.models import Client as Tg_client

logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s %(levelname) -8s %(message)s',
    level=settings.LOG_LEVEL,
    datefmt='%Y.%m.%d %I:%M:%S',
    handlers=[
        logging.StreamHandler(stream=sys.stderr)
    ],
)


async def main():
    """ Автоответчик """

    """ Пул сессий """

    # apps = [Client(x.session_aa.name.split('/')[-1].split('.')[0]) for x in Account.objects.filter(
    #     status=True, is_auto_answering_active=True, session_aa__isnull=False).order_by('first_name')]

    apps = []
    accounts = Account.objects.filter(status=True, is_auto_answering_active=True).order_by('first_name')
    for account in accounts:
        if account.session_aa:
            apps.append(Client(account.session_aa.name.split('/')[-1].split('.')[0]))

    logger.info(apps)
    for app in apps:

        @app.on_message(filters.text & filters.private)
        async def auto_answering_handler(client, message):
            account = Account.objects.filter(session_aa=f'sessions/{client.name}.session').last()
            tg_cli = Tg_client.objects.filter(user_id=message.from_user.id, account=account).last()
            logger.info(f'[{message.text}] [{account}] [{tg_cli}] [NOT AUTOANSWERING]')

            """
                * Ответ пользователю
                * Создание объекта клиента
            """
            try:
                if tg_cli.first_name == 'Admin66':
                    await client.send_message(message.chat.id, '[DEBUG] [AUTOANSWERING]')
            except:
                pass
            if not tg_cli:
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
        logger.info(f'[{Account.objects.filter(session_aa=f"sessions/{app.name}.session").last()}] [{app.name}] [started]')

    """ Активируем клиенты pyrogram с помощью compose() """
    await compose(apps, False)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except sqlite3.OperationalError as e:
        print(e)
    except KeyboardInterrupt:
        sys.exit(0)