import asyncio
import os
import random
import sys
from datetime import datetime

from django.conf import settings
from pyrogram import Client, errors

from apps.spamer.models import Account

client_parameters = [
    {
        "device_model": "iPhone 12",
        "app_version": "1.0.0",
        "system_version": "iOS 14.4",
        "lang_code": "ru"
    },
    {
        "device_model": "Samsung Galaxy S21",
        "app_version": "2.0.0",
        "system_version": "Android 11",
        "lang_code": "ru"
    },
    {
        "device_model": "POCO X3 Pro",
        "app_version": "1.1.0",
        "system_version": "Android 12",
        "lang_code": "ru"
    },
    {
        "device_model": "MacBook Pro",
        "app_version": "1.2.3",
        "system_version": "macOS Big Sur",
        "lang_code": "ru"
    },
    {
        "device_model": "iPhone 11",
        "app_version": "2.1.0",
        "system_version": "iOS 14.3",
        "lang_code": "ru"
    },
    {
        "device_model": "OnePlus 9",
        "app_version": "3.0.0",
        "system_version": "Android 12",
        "lang_code": "ru"
    },
    {
        "device_model": "iPad Pro",
        "app_version": "1.0.1",
        "system_version": "iPadOS 14.5",
        "lang_code": "ru"
    },
    {
        "device_model": "Sony Xperia",
        "app_version": "4.0.0",
        "system_version": "Android 10",
        "lang_code": "ru"
    },
    {
        "device_model": "iPhone 7 Plus",
        "app_version": "1.3.0",
        "system_version": "iOS 11.1",
        "lang_code": "ru"
    },
    {
        "device_model": "HTC One",
        "app_version": "5.0.0",
        "system_version": "Android 9",
        "lang_code": "ru"
    },
    {
        "device_model": "Nexus 5",
        "app_version": "1.4.1",
        "system_version": "Android 10",
        "lang_code": "ru"
    }
]


# Создание и активация сессий
async def create_session_for_chat():

    phone_number = Account.objects.filter(is_activated=False).last().phone

    chat = 'for_chat'

    session_name = f"session_{str(datetime.now().strftime('%Y%m%d_%H%M'))}_{chat}"
    params = random.choice(client_parameters)
    try:

        client = Client(session_name, api_id=settings.API_ID, api_hash=settings.API_HASH,
                        phone_number=phone_number,
                        device_model=params['device_model'],
                        app_version=params['app_version'],
                        system_version=params['system_version'],
                        lang_code=params['lang_code'])
        await client.connect()
        code = await client.send_code(phone_number)
        phone_code_hash = code.phone_code_hash
        await client.sign_in(phone_number=phone_number,
                             phone_code_hash=phone_code_hash,
                             phone_code='sms_code')

        phone_code_hash = code.phone_code_hash
        await client.disconnect()
        await asyncio.sleep(5)
        print(f"Сессия {session_name} успешно активирована!")
    except errors.PhoneNumberInvalid:
        print(f"Неверный номер телефона для сессии {session_name}.")
    except errors.PhoneCodeInvalid:
        print(f"Неверный код подтверждения для сессии {session_name}.")
    except errors.PhoneNumberBanned:
        print(f"Номер телефона забанен для сессии {session_name}.")
    except Exception as e:
        print(f"Ошибка при активации сессии {session_name}: {e}")


# Основная функция
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(create_session_for_chat())
    loop.run_forever()
