import asyncio
import os

import pyrogram
import pyinotify

path_to = "/var/www/html/inpost/telegram_bot"

class MyEventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        # Get the absolute path of the newly created file
        file_path = event.pathname

        # Extract the filename
        file_name = file_path.split('/')[-1].split('.')[0]

        print(f"New file created: {file_name}")

        # os.system(f'python test.py {file_name}')

        # # Инициализируем клиента Pyrogram с помощью сессионного файла
        # client = pyrogram.Client(name=file_name)
        # with client:
        #     # Получаем информацию о пользователе
        #     user = client.get_me()
        #     first_name = user.first_name
        #     last_name = user.last_name
        #     user_id = user.id
        #     username = user.username
        #
        # print(f"Имя пользователя: {first_name} {last_name}")
        # print(f"ID пользователя: {user_id}")
        # print(f"Username пользователя: @{username}")

# Create an instance of the event handler
handler = MyEventHandler()

# Create a watcher with the handler
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, handler)

# Watch the directory for file creation events
wm.add_watch(path_to, pyinotify.IN_CREATE)

# Start the notifier to monitor for events
notifier.loop()
