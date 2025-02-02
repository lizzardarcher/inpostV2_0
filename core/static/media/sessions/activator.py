import datetime
import os
import traceback
from time import sleep

import django
from django.core.files import File
from pyrogram import Client

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import Account, GeneralSettings, AccountLogging

directory_to_list = '/var/www/html/inpost/core/static/media/sessions'


def list_files_in_directory(directory_path):
    """Lists all files in a given directory.
    Args:
        directory_path: The path to the directory to list files from.
    Returns:
        A list of file names within the directory.
    """

    files = []
    for filename in os.listdir(directory_path):
        # Check if the current item is a file (not a directory)
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            files.append(filename)

    return files


while True:
    file_list = list_files_in_directory(directory_to_list)
    accounts = Account.objects.filter(status=True, is_activated=False) | Account.objects.filter(status=True, is_change_needed=True)
    print('Pending accounts:', accounts, len(accounts))
    for account in accounts:
        try:
            acc = Account.objects.filter(session=account.session)

            for file in file_list:

                #  Если аккаунт ещё не активирован
                if account.session.name.split('/')[-1] == file:

                    os.system('systemctl stop spamerv2.service ')
                    # os.system('systemctl stop autoanswering.service')
                    sleep(1)
                    if not account.is_activated:

                        session_for_chat = file.replace('.', '_for_chat.')

                        client = Client(name=file.split('.')[0])
                        with client:
                            # Получаем информацию о пользователе
                            user = client.get_me()
                            print(user)
                            try:
                                profile_photo = user.photo.big_file_id
                                # Download the photo
                                photo_bytes = client.download_media(profile_photo,
                                                    file_name=f'/var/www/html/inpost/core/static/media/{profile_photo}.jpg')
                                # Create a file object from the photo bytes
                                photo_file = File(open(photo_bytes, 'rb'), name=f'{profile_photo}.jpg')
                            except:
                                photo_file = None

                            user_id = user.id
                            try:
                                first_name = user.first_name
                            except AttributeError:
                                first_name = None
                            try:
                                last_name = user.last_name
                            except AttributeError:
                                last_name = None
                            try:
                                username = user.username
                            except AttributeError:
                                username = None
                            try:
                                bio = user.bio
                            except AttributeError:
                                bio = None
                        acc.update(is_activated=True, first_name=first_name, last_name=last_name, username=username,
                                   id_account=user_id, photo=photo_file, is_auto_answering_active=False, bio=bio,
                                   is_change_needed=False)
                        break

                    elif account.is_change_needed:
                        client = Client(name=file.split('.')[0])
                        first_name = account.first_name
                        last_name = account.last_name
                        username = account.username
                        bio = account.bio
                        photo = f'/var/www/html/inpost/core/static/media/{account.photo}'
                        with client:
                            client.update_profile(first_name=first_name, last_name=last_name, bio=bio)
                            client.set_profile_photo(photo=open(photo, 'rb'))
                            try:
                                client.set_username(username)
                            except: ...
                        acc.update(is_change_needed=False)
                        break

                    os.system('systemctl start spamerv2.service ')
                    sleep(1)
                    # os.system('systemctl start testspamer.service')
                    # os.system('systemctl start autoanswering.service')
                    # todo GeneralSettings handler
                    # GeneralSettings.objects.filter(id=1).update(is_reload_spam_needed=True)
        except:
            if '[401 AUTH_KEY_UNREGISTERED]' in traceback.format_exc():
                acc.update(is_activated=True, is_change_needed=False, status=False)
                AccountLogging.objects.create(log_level='Fatal', account=acc.last(), user=acc.last().user,
                                              message='[401 AUTH_KEY_UNREGISTERED] необходимо создать сессию заново',
                                              datetime=datetime.datetime.now())
            else:
                acc.update(is_activated=True, is_change_needed=False, status=False)
                AccountLogging.objects.create(log_level='Fatal', account=acc.last(), user=acc.last().user,
                                              message=f'{traceback.format_exc()}',
                                              datetime=datetime.datetime.now())
            print(traceback.format_exc())
        # todo GeneralSettings handler
        # GeneralSettings.objects.filter(id=1).update(is_reload_spam_needed=True)
    sleep(5)

