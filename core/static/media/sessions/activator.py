import os
from time import sleep

import django
from django.core.files import File
from pyrogram import Client

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from apps.spamer.models import Account

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
    accounts = Account.objects.filter(is_activated=False) | Account.objects.filter(is_change_needed=True)
    print('Pending accounts:', accounts, len(accounts))
    for account in accounts:

        acc = Account.objects.filter(session=account.session)

        for file in file_list:

            #  Если аккаунт ещё не активирован
            if account.session.name.split('/')[-1] == file:

                if not account.is_activated:
                    client = Client(name=file.split('.')[0])
                    with client:
                        # Получаем информацию о пользователе
                        user = client.get_me()

                        profile_photo = user.photo.big_file_id
                        print(user.photo)

                        # Download the photo
                        photo_bytes = client.download_media(profile_photo,
                                            file_name=f'/var/www/html/inpost/core/static/media/{profile_photo}.jpg')
                        print(photo_bytes)

                        # Create a file object from the photo bytes
                        photo_file = File(open(photo_bytes, 'rb'), name=f'{profile_photo}.jpg')
                        print(photo_file)

                        first_name = user.first_name
                        last_name = user.last_name
                        user_id = user.id
                        username = user.username
                    acc.update(is_activated=True, first_name=first_name, last_name=last_name, username=username,
                               id_account=user_id, photo=photo_file, )
                    acc.update(is_change_needed=False)

                    break

                elif account.is_change_needed:
                    client = Client(name=file.split('.')[0])
                    first_name = account.first_name
                    last_name = account.last_name
                    photo = f'/var/www/html/inpost/core/static/media/{account.photo}'
                    print('[PHOTO]',photo)
                    with client:
                        client.update_profile(first_name=first_name, last_name=last_name,)
                        client.set_profile_photo(photo=open(photo, 'rb'))
                    acc.update(is_change_needed=False)
                    break

    sleep(5)
