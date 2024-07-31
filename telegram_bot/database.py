import sqlite3 as sql
from sqlite3 import Error
import traceback
from config import db


def create_connection():
    connection = None
    try:
        connection = sql.connect(db)
    except Error as e:
        print(e)
    return connection


DB_CONNECTION = None
CURSOR = None
# dayofweek = 'mon_stat_subs'


def connect():
    global DB_CONNECTION, CURSOR
    DB_CONNECTION = create_connection()
    CURSOR = DB_CONNECTION.cursor()


connect()

CREATE_NOTIFICATION = 'INSERT INTO home_notification (text, user_id) VALUES (?, ?)'

GET_ALL_USERS = 'SELECT * FROM auth_user'
GET_ALL_POSTS = 'SELECT * FROM home_post'
GET_ALL_CHATS = 'SELECT * FROM home_chat'
GET_ALL_BOTS = 'SELECT * FROM home_bot'
GET_ALL_SCHEDULE = 'SELECT * FROM home_postschedule'
GET_ALL_TEMPLATES = 'SELECT * FROM home_template'
GET_CHAT_FOR_STATS = 'SELECT chat_type, ref, id, subscribers, negative_subs, positive_subs FROM home_chat'

GET_CHAT_REF_TITLE = 'SELECT ref, title FROM home_chat WHERE chat_id=0'
GET_BOT_TOKEN = 'SELECT token FROM home_bot'

GET_SCH_BY_USER_ID_NOT_SENT = 'SELECT schedule, post_id, user_id, id FROM home_postschedule WHERE user_id=? and is_sent=?'
GET_CHAT_BY_USER_ID = 'SELECT ref, title, chat_id, bot_id  FROM home_chat WHERE user_id=?'
GET_POST_BY_ID = 'SELECT text, photo_1, photo_2, photo_3 ,photo_4, photo_5, url, url_text, video, btn_name_1, btn_name_2, btn_name_3, btn_name_4, template_id, name, document, music FROM home_post WHERE id=?'
GET_BOT_BY_USER_ID = 'SELECT * FROM home_bot WHERE user_id=?'
GET_TEMPLATE_BY_ID = 'SELECT * FROM home_template WHERE id=?'
GET_TZ = 'SELECT tz FROM home_userstatus WHERE user_id=?'

UPDATE_TZ = 'UPDATE home_userstatus SET tz=? WHERE user_id=?'
UPDATE_SCHED_SET_SENT = 'UPDATE home_postschedule SET is_sent=? WHERE id=?'
UPDATE_CHAT_STATS = 'UPDATE home_chat SET {0}=? WHERE id=?'
UPDATE_CHAT_INC = 'UPDATE home_chat SET positive_subs=? WHERE id=?'
UPDATE_CHAT_DEC = 'UPDATE home_chat SET negative_subs=? WHERE id=?'
UPDATE_CHAT_SUBS = 'UPDATE home_chat SET subscribers=? WHERE id=?'
UPDATE_CHAT_ID = 'UPDATE home_chat SET chat_id=? WHERE title=?'

RESET_INC_DEC = 'UPDATE home_chat SET negative_subs=?, positive_subs=? WHERE id=?'


def create(connection, query, value):
    try:
        with sql.connect(db, check_same_thread=False, timeout=100) as con:
            cursor = con.cursor()
            cursor.execute(query, value)
            con.commit()
    except Error:
        print(traceback.format_exc())
    return True


def get_all(connection, query, *args):
    try:
        with sql.connect(db, check_same_thread=False, timeout=100) as con:
            cursor = con.cursor()
            data = cursor.execute(query).fetchall()
    except Error:
        print(Error)
        print(traceback.format_exc())
    return data


def get_by_id(connection, query, value):
    try:
        with sql.connect(db, check_same_thread=False, timeout=100) as con:
            cursor = con.cursor()
            data = cursor.execute(query, value).fetchall()
    except Error:
        print(Error)
    return data


def update(connection, query, value):
    try:
        with sql.connect(db, check_same_thread=False, timeout=100) as con:
            cursor = con.cursor()
            cursor.execute(query, value)
            con.commit()
    except Error:
        print(Error)
    return True


def update_chat_stats(connection, query, day, value):
    try:
        with sql.connect(db, check_same_thread=False, timeout=100) as con:
            cursor = con.cursor()
            cursor.execute(query.format(day), value)
            con.commit()
    except Error:
        traceback.format_exc()
    return True
