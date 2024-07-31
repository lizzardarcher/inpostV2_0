import os
import traceback
from datetime import datetime, timedelta
from time import sleep

from telebot import TeleBot
from telebot.types import (InputMediaPhoto, InputMediaVideo,
                           InputMediaAudio, InputMediaDocument,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup, )

import django_orm
from apps.home.models import *
from django.contrib.auth.models import User

if os.name == 'nt':
    MEDIA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\core\\static\\media" + "\\"
else:
    MEDIA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/core/static/media" + "/"
hr = '_______________________________\n'


def auto_post():
    # получить всех юзеров
    users = User.objects.all()

    for user in users:
        user_id = user.id

        # цикл - получить расписание неотправленных постов с каждым юзером
        schedule = PostSchedule.objects.filter(user=user, is_sent=False)

        for sched in schedule:
            sched_datetime = datetime.strptime(str(sched.schedule), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            post_id = sched.post.id
            sched_id = sched.id
            try:
                tz = int(
                    UserStatus.objects.filter(user=user)[0][0].split()[0].replace('+', '').replace('-', '')
                )
            except:
                tz = 6

            datetime_now = (datetime.now() + timedelta(hours=tz - 6)).strftime('%Y-%m-%d %H:%M')

            # Проверка по дате-времени, если совпадает, то continue

            if datetime_now == sched_datetime:
                print(sched_datetime, datetime_now, sched_datetime == datetime_now)
                print('OK!')

                # цикл - по чатам с user_id
                chats = Chat.objects.filter(user=user)

                for chat in chats:
                    chat_username = '@' + chat.ref.split('/')[-1]
                    chat_id = chat.chat_id
                    bot_for_chat = chat.bot.id

                    # Цикл по ботам с user_id
                    bots = Bot.objects.filter(user=user)

                    for bot in bots:
                        bot_token = bot.token
                        bot_id = bot.id

                        # цикл по постам c user_id
                        post = Post.objects.get(id=post_id)

                        if bot_id == bot_for_chat:
                            text = str(post.text).replace('<p>', '').replace('</p>', '').replace('<br />', '').replace(
                                '<br>', '').replace('&nbsp;', '')
                            # print(text)
                            try:
                                template = Template.objects.get(id=post.template.id).text.replace(
                                    '<p>', '').replace('</p>', '').replace('<br />', '').replace('<br>', '')
                                text = text + hr + template
                                # print('template', template)
                            except: ...

                            photo_list = []
                            if post.photo_1: photo_list.append(str(post.photo_1.path))
                            if post.photo_2: photo_list.append(str(post.photo_2.path))
                            if post.photo_3: photo_list.append(str(post.photo_3.path))
                            if post.photo_4: photo_list.append(str(post.photo_4.path))
                            if post.photo_5: photo_list.append(str(post.photo_5.path))

                            # print(photo_list)
                            url_btn = []
                            if post.url: url_btn.append(post.url)
                            if post.url_text: url_btn.append(post.url_text)

                            video = ''
                            if post.video: video = post.video

                            document = ''
                            if post.document: document = post.document

                            music = ''
                            if post.music: music = post.music

                            markup = InlineKeyboardMarkup()

                            if url_btn:
                                markup.row_width = 2
                                markup.add(
                                    InlineKeyboardButton(text=url_btn[1], url=url_btn[0], callback_data="...")
                                )
                            btn_list = []
                            if post.btn_name_1: btn_list.append(post.btn_name_1)
                            if post.btn_name_2: btn_list.append(post.btn_name_2)
                            if post.btn_name_3: btn_list.append(post.btn_name_3)
                            if post.btn_name_4: btn_list.append(post.btn_name_4)

                            if btn_list:
                                if len(btn_list) == 1:
                                    markup.add(InlineKeyboardButton(text=btn_list[0], callback_data="...", ))
                                if len(btn_list) == 2:
                                    markup.add(
                                        InlineKeyboardButton(text=btn_list[0], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[1], callback_data="...", ),
                                    )
                                if len(btn_list) == 3:
                                    markup.add(
                                        InlineKeyboardButton(text=btn_list[0], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[1], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[2], callback_data="...", ),
                                    )
                                if len(btn_list) == 4:
                                    markup.add(
                                        InlineKeyboardButton(text=btn_list[0], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[1], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[2], callback_data="...", ),
                                        InlineKeyboardButton(text=btn_list[3], callback_data="...", ),
                                    )

                            # START POST ###############################################################################
                            ############################################################################################

                            # Отправить сообщение только текст
                            try:

                                bot = TeleBot(bot_token)
                                notification_success = f'✅ {post.name} отправлен в {chat.title} {datetime_now}'

                                if not photo_list and not video and not music and not document:
                                    bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML',
                                                     reply_markup=markup)
                                    PostSchedule.objects.filter(id=sched_id).update(is_sent=True)
                                    Notification.objects.create(text=notification_success, user=user)

                                # Отправить сообщение фото
                                elif photo_list and not video:
                                    if len(photo_list) == 1:
                                        bot.send_photo(chat_id=chat_id, photo=open(photo_list[0], 'rb'), caption=text,
                                                       parse_mode='HTML', reply_markup=markup)
                                    elif len(photo_list) == 2:

                                        bot.send_media_group(chat_id=chat_id, media=[
                                            InputMediaPhoto(media=open(photo_list[0], 'rb'), caption=text, parse_mode='HTML'),
                                            InputMediaPhoto(media=open(photo_list[1], 'rb')), ])
                                    elif len(photo_list) == 3:

                                        bot.send_media_group(chat_id=chat_id, media=[
                                            InputMediaPhoto(media=open(photo_list[0], 'rb'), caption=text, parse_mode='HTML'),
                                            InputMediaPhoto(media=open(photo_list[1], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[2], 'rb')), ])
                                    elif len(photo_list) == 4:
                                        print(photo_list)
                                        bot.send_media_group(chat_id=chat_id, media=[
                                            InputMediaPhoto(media=open(photo_list[0], 'rb'), caption=text,
                                                            parse_mode='HTML'),
                                            InputMediaPhoto(media=open(photo_list[1], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[2], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[3], 'rb')), ])
                                    elif len(photo_list) == 5:

                                        bot.send_media_group(chat_id=chat_id, media=[
                                            InputMediaPhoto(media=open(photo_list[0], 'rb'), caption=text,
                                                            parse_mode='HTML'),
                                            InputMediaPhoto(media=open(photo_list[1], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[2], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[3], 'rb')),
                                            InputMediaPhoto(media=open(photo_list[4], 'rb')), ])
                                    PostSchedule.objects.filter(id=sched_id).update(is_sent=True)
                                    Notification.objects.create(text=notification_success, user=user)

                                # Отправить сообщение видео
                                elif video and not photo_list:
                                    bot.send_video(chat_id=chat_id, video=open(video, 'rb'),
                                                   caption=text, parse_mode='HTML', reply_markup=markup)
                                    PostSchedule.objects.filter(id=sched_id).update(is_sent=True)
                                    Notification.objects.create(text=notification_success, user=user)

                                # Отправить сообщение документ
                                elif document and not music and not photo_list and not video:
                                    bot.send_document(chat_id=chat_id,
                                                      document=open(document, 'rb'), caption=text,
                                                      parse_mode='HTML', reply_markup=markup)
                                    PostSchedule.objects.filter(id=sched_id).update(is_sent=True)
                                    Notification.objects.create(text=notification_success, user=user)

                                # Отправить сообщение аудио
                                elif music and not document and not photo_list and not video:
                                    bot.send_audio(chat_id=chat_id, audio=open(music, 'rb'),
                                                   caption=text, parse_mode='HTML', reply_markup=markup)
                                    PostSchedule.objects.filter(id=sched_id).update(is_sent=True)
                                    Notification.objects.create(text=notification_success, user=user)
                                sleep(0.4)
                                print(notification_success)
                            except Exception as e:
                                notification_fail = f'🛑 Ошибка отправки {post.name} в {chat.title} {datetime_now}'
                                if '403' not in traceback.format_exc():
                                    Notification.objects.create(text=notification_fail, user=user)
                                print(e)
                                print(notification_fail)

while True:
    auto_post()
    sleep(1)
