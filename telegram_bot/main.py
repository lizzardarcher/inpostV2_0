from telebot import TeleBot
from telebot.types import (InputMediaPhoto, InputMediaVideo,
                           InputMediaAudio, InputMediaDocument,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButton, ReplyKeyboardMarkup, )
from database import (get_all, get_by_id, DB_CONNECTION, GET_ALL_USERS,
                      GET_SCH_BY_USER_ID_NOT_SENT, GET_CHAT_BY_USER_ID,
                      GET_BOT_BY_USER_ID, GET_POST_BY_ID, GET_TEMPLATE_BY_ID, UPDATE_SCHED_SET_SENT,
                      update, create, CREATE_NOTIFICATION, UPDATE_TZ, GET_TZ, )
from datetime import datetime, timedelta
import traceback
from time import sleep
import os

if os.name == 'nt':
    MEDIA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "\\core\\static\\media" + "\\"
else:
    MEDIA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/core/static/media" + "/"
hr = '_______________________________\n'


def auto_post():
    # получить всех юзеров
    users = get_all(DB_CONNECTION, GET_ALL_USERS)
    for user in users:
        user_id = user[0]
        # print(user)

        # цикл - получить расписание неотправленных постов с каждым юзером
        schedule = get_by_id(DB_CONNECTION, GET_SCH_BY_USER_ID_NOT_SENT, (user_id, False))
        for sched in schedule:
            sched_datetime = datetime.strptime(sched[0], '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M')
            post_id = sched[1]
            sched_id = sched[3]
            # print(sched)
            # print(get_by_id(DB_CONNECTION, GET_TZ, (user_id,))[0][0].split()[0].replace('+', '').replace('-', ''))
            # TODO UTC
            # print(datetime.now())
            try:
                tz = int(
                    get_by_id(DB_CONNECTION, GET_TZ, (user_id,))[0][0].split()[0].replace('+', '').replace('-', ''))
            except:
                tz = 6
            # tz_data = get_by_id(DB_CONNECTION, GET_TZ, (user_id,))
            datetime_now = (datetime.now() + timedelta(hours=tz - 6)).strftime('%Y-%m-%d %H:%M')
            # print(datetime_now)
            # print((datetime.now()+timedelta(hours=tz-6)).strftime('%Y-%m-%d %H:%M'))

            # Проверка по дате-времени, если совпадает, то continue
            # print(tz)
            # print((datetime.now()+timedelta(hours=tz-6)).strftime('%Y-%m-%d %H:%M'), sched_datetime, tz_data)
            # sleep(1)
            if (datetime.now() + timedelta(hours=tz - 6)).strftime('%Y-%m-%d %H:%M') == sched_datetime:
                # print('OK!')

                # цикл - по чатам с user_id
                chats = get_by_id(DB_CONNECTION, GET_CHAT_BY_USER_ID, (user_id,))
                for chat in chats:
                    chat_username = '@' + chat[0].split('/')[-1]
                    chat_id = chat[2]
                    bot_for_chat = chat[3]
                    # print(chat_username)

                    # Цикл по ботам с user_id
                    bots = get_by_id(DB_CONNECTION, GET_BOT_BY_USER_ID, (user_id,))
                    for bot in bots:
                        # print(bot[4])
                        bot_token = bot[0]
                        bot_id = bot[1]

                        # цикл по постам c user_id
                        post = get_by_id(DB_CONNECTION, GET_POST_BY_ID, (post_id,))[0]

                        # print('bot_id == bot_for_chat', bot_id, bot_for_chat, bot_id == bot_for_chat)
                        if bot_id == bot_for_chat:
                            text = str(post[0]).replace('<p>', '').replace('</p>', '').replace('<br />', '').replace(
                                '<br>', '').replace('&nbsp;', '')

                            template_id = post[13]
                            if template_id:
                                template = get_by_id(DB_CONNECTION, GET_TEMPLATE_BY_ID, (template_id,))[0][3].replace(
                                    '<p>', '').replace('</p>', '').replace('<br />', '').replace('<br>', '')
                                text = text + hr + template

                            photo_list = []
                            if post[1]: photo_list.append(post[1])
                            if post[2]: photo_list.append(post[2])
                            if post[3]: photo_list.append(post[3])
                            if post[4]: photo_list.append(post[4])
                            if post[5]: photo_list.append(post[5])

                            # print(photo_list)
                            url_btn = []
                            if post[6]: url_btn.append(post[6])
                            if post[7]: url_btn.append(post[7])

                            video = ''
                            if post[8]: video = post[8]

                            document = ''
                            if post[15]: document = post[15]

                            music = ''
                            if post[16]: music = post[16]

                            markup = InlineKeyboardMarkup()
                            if url_btn:
                                markup.row_width = 2
                                markup.add(
                                    InlineKeyboardButton(text=url_btn[1], url=url_btn[0], callback_data="...")
                                )
                            btn_list = []
                            if post[9]: btn_list.append(post[9])
                            if post[10]: btn_list.append(post[10])
                            if post[11]: btn_list.append(post[11])
                            if post[12]: btn_list.append(post[12])

                            # Todo handle btn count
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

                            # START POST ###################################################################################
                            ################################################################################################

                            # Отправить сообщение только текст
                            try:

                                bot = TeleBot(bot_token)
                                notification_success = f'{post[14]} отправлен в {chat[1]} {datetime_now}'
                                notification_fail = f'Ошибка отправки {post[14]} в {chat[1]} {datetime_now}'

                                print('Try sending to ', chat_username, bot_token)

                                if not photo_list and not video and not music and not document:
                                    bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML',
                                                     reply_markup=markup)
                                    update(DB_CONNECTION, UPDATE_SCHED_SET_SENT, (True, sched_id))
                                    create(DB_CONNECTION, CREATE_NOTIFICATION, (notification_success, user_id))

                                # Отправить сообщение фото
                                elif photo_list and not video:
                                    if len(photo_list) == 1:
                                        with open(MEDIA_DIR + photo_list[0], 'rb') as media_1:
                                            bot.send_photo(chat_id=chat_id, photo=media_1, caption=text,
                                                           parse_mode='HTML', reply_markup=markup)
                                    elif len(photo_list) == 2:
                                        with open(MEDIA_DIR + photo_list[0], 'rb') as media_1:
                                            with open(MEDIA_DIR + photo_list[1], 'rb') as media_2:
                                                bot.send_media_group(chat_id=chat_id, media=[
                                                    InputMediaPhoto(media=media_1, caption=text, parse_mode='HTML'),
                                                    InputMediaPhoto(media=media_2), ])
                                    elif len(photo_list) == 3:
                                        with open(MEDIA_DIR + photo_list[0], 'rb') as media_1:
                                            with open(MEDIA_DIR + photo_list[1], 'rb') as media_2:
                                                with open(MEDIA_DIR + photo_list[2], 'rb') as media_3:
                                                    bot.send_media_group(chat_id=chat_id, media=[
                                                        InputMediaPhoto(media=media_1, caption=text, parse_mode='HTML'),
                                                        InputMediaPhoto(media=media_2),
                                                        InputMediaPhoto(media=media_3), ])
                                    elif len(photo_list) == 4:
                                        with open(MEDIA_DIR + photo_list[0], 'rb') as media_1:
                                            with open(MEDIA_DIR + photo_list[1], 'rb') as media_2:
                                                with open(MEDIA_DIR + photo_list[2], 'rb') as media_3:
                                                    with open(MEDIA_DIR + photo_list[3], 'rb') as media_4:
                                                        bot.send_media_group(chat_id=chat_id, media=[
                                                            InputMediaPhoto(media=media_1, caption=text,
                                                                            parse_mode='HTML'),
                                                            InputMediaPhoto(media=media_2),
                                                            InputMediaPhoto(media=media_3),
                                                            InputMediaPhoto(media=media_4), ])
                                    elif len(photo_list) == 5:
                                        with open(MEDIA_DIR + photo_list[0], 'rb') as media_1:
                                            with open(MEDIA_DIR + photo_list[1], 'rb') as media_2:
                                                with open(MEDIA_DIR + photo_list[2], 'rb') as media_3:
                                                    with open(MEDIA_DIR + photo_list[3], 'rb') as media_4:
                                                        with open(MEDIA_DIR + photo_list[4], 'rb') as media_5:
                                                            bot.send_media_group(chat_id=chat_id, media=[
                                                                InputMediaPhoto(media=media_1, caption=text,
                                                                                parse_mode='HTML'),
                                                                InputMediaPhoto(media=media_2),
                                                                InputMediaPhoto(media=media_3),
                                                                InputMediaPhoto(media=media_4),
                                                                InputMediaPhoto(media=media_5), ])
                                    update(DB_CONNECTION, UPDATE_SCHED_SET_SENT, (True, sched_id))
                                    create(DB_CONNECTION, CREATE_NOTIFICATION, (notification_success, user_id))

                                # Отправить сообщение видео
                                elif video and not photo_list:
                                    with open(MEDIA_DIR + video, 'rb') as media:
                                        bot.send_video(chat_id=chat_id, video=media,
                                                       caption=text, parse_mode='HTML', reply_markup=markup)
                                        update(DB_CONNECTION, UPDATE_SCHED_SET_SENT, (True, sched_id))
                                        create(DB_CONNECTION, CREATE_NOTIFICATION, (notification_success, user_id))

                                # Отправить сообщение документ
                                elif document and not music and not photo_list and not video:
                                    with open(MEDIA_DIR + document, 'rb') as media:
                                        bot.send_document(chat_id=chat_id,
                                                          document=media, caption=text,
                                                          parse_mode='HTML', reply_markup=markup)
                                        update(DB_CONNECTION, UPDATE_SCHED_SET_SENT, (True, sched_id))
                                        create(DB_CONNECTION, CREATE_NOTIFICATION, (notification_success, user_id))

                                # Отправить сообщение аудио
                                elif music and not document and not photo_list and not video:
                                    with open(MEDIA_DIR + music, 'rb') as media:
                                        bot.send_audio(chat_id=chat_id, audio=media,
                                                       caption=text, parse_mode='HTML', reply_markup=markup)
                                        update(DB_CONNECTION, UPDATE_SCHED_SET_SENT, (True, sched_id))
                                        create(DB_CONNECTION, CREATE_NOTIFICATION, (notification_success, user_id))
                                print('Success! Message sent ', chat_username)
                                sleep(0.4)

                            except Exception as e:
                                if '403' not in traceback.format_exc():
                                    create(DB_CONNECTION, CREATE_NOTIFICATION, ('DEBUG ' + notification_fail, user_id))
                                print('Fail to send to ', chat_username, bot_token)
                                print(e)


while True:
    auto_post()
    sleep(1)
