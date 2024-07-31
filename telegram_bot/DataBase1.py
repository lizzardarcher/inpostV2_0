import utils.config as cnfg
from sqlite3 import Error

if cnfg.DEBUG:
    from sqlite3 import connect as sqlite3_connect
    from sqlite3 import Error
else:
    from pymysql import connect as pymysql_connect
    from mysql.connector import Error

''' 
ТАБЛИЦЫ ДАННЫХ
'''
USR_TBL_NAME = 'Users'

User_id = 'ID'  # id пользователя
User_email = 'Email_пользователя'  # email пользователя (уникальный ключ в базе)
User_phone = 'Номер_телефона'  # телефон пользователя
User_password = 'Пароль'  # пароль пользователя
User_referer = 'Кто_пригласил'  # реферер (кто пригласил) пользователя
User_lang = 'Язык'  # язык пользователя
Wallet_balance = 'Баланс'  # баланс пользователя
Wallet_total = 'Всего'  # всего заработано
Wallet_return = 'Оборот'  # сумма всех проданных торговых систем

if cnfg.DEBUG:
    USERS_TABLE = f'''CREATE TABLE IF NOT EXISTS {USR_TBL_NAME} (
                    {User_id} INTEGER PRIMARY KEY,
                    {User_email} TEXT NULL,
                    {User_phone} TEXT NULL,
                    {User_password} TEXT,
                    {User_referer} INTEGER,
                    {User_lang} TEXT,
                    {Wallet_balance} INTEGER DEFAULT 0,
                    {Wallet_total} INTEGER DEFAULT 0,
                    {Wallet_return} INTEGER DEFAULT 0
                )'''
else:
    USERS_TABLE = f'''CREATE TABLE IF NOT EXISTS {USR_TBL_NAME} (
                    {User_id} BIGINT NOT NULL,
                    {User_email} TEXT NOT NULL,
                    {User_phone} TEXT NULL,
                    {User_password} TEXT,
                    {User_referer} BIGINT,
                    {User_lang} TEXT,
                    {Wallet_balance} BIGINT DEFAULT 0,
                    {Wallet_total} BIGINT DEFAULT 0,
                    {Wallet_return} BIGINT DEFAULT 0,
                    PRIMARY KEY ({User_id})
                )'''

''' 
ЗАПРОСЫ SQL
'''
if cnfg.DEBUG:  # SQLite (локальная)
    DB_NAME = 'Crypto_bot'
    val = '?'
else:  # MySQL (хост)
    DB_NAME = 'xx_Crypto_bot'
    MYSQL_DB_HOST = 'localhost'
    MYSQL_DB_USER = 'xx'
    MYSQL_DB_PASSWORD = 'xx'
    val = '%s'

SET_NEW_USER = f'''INSERT INTO {USR_TBL_NAME} ({User_referer}, {User_id}) VALUES({val}, {val})'''
GET_USER = f'''SELECT {User_id} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

UPDATE_ID_USER_EMAIL = f'''UPDATE {USR_TBL_NAME} SET {User_id} = {val} WHERE {User_email} = {val}'''
UPDATE_ID_USER_PHONE = f'''UPDATE {USR_TBL_NAME} SET {User_id} = {val} WHERE {User_phone} = {val}'''
GET_ID_ALL_USERS = f'''SELECT {User_id} FROM {USR_TBL_NAME}'''
GET_COUNT_USERS = f'''SELECT COUNT(*) as count FROM {USR_TBL_NAME}'''
DELETE_USER = f'''DELETE FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

GET_COUNT_REFERALS = f'''SELECT COUNT(*) as "count" FROM {USR_TBL_NAME} WHERE {User_referer} = ?'''
GET_IDS_REFERALS = f'''SELECT {User_id} FROM {USR_TBL_NAME} WHERE {User_referer} = ?'''

SET_USER_REFERER = f'''UPDATE {USR_TBL_NAME} SET {User_referer} = {val} WHERE {User_id} = {val}'''
GET_USER_REFERER = f'''SELECT {User_referer} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

SET_USER_EMAIL = f'''UPDATE {USR_TBL_NAME} SET {User_email} = {val} WHERE {User_id} = {val}'''
GET_USER_EMAIL = f'''SELECT {User_email} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''
CHECK_EMAIL_USER = f'''SELECT {User_email} FROM {USR_TBL_NAME} WHERE {User_email} = {val}'''
CHECK_PHONE_USER = f'''SELECT {User_phone} FROM {USR_TBL_NAME} WHERE {User_phone} = {val}'''

SET_USER_PHONE = f'''UPDATE {USR_TBL_NAME} SET {User_phone} = {val} WHERE {User_id} = {val}'''
GET_USER_PHONE = f'''SELECT {User_phone} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

SET_USER_PASSWORD = f'''UPDATE {USR_TBL_NAME} SET {User_password} = {val} WHERE {User_id} = {val}'''
GET_USER_PASSWORD_EMAIL = f'''SELECT {User_password} FROM {USR_TBL_NAME} WHERE {User_email} = {val}'''
GET_USER_PASSWORD_PHONE = f'''SELECT {User_password} FROM {USR_TBL_NAME} WHERE {User_phone} = {val}'''

SET_USER_LANG = f'''UPDATE {USR_TBL_NAME} SET {User_lang} = {val} WHERE {User_id} = {val}'''
GET_USER_LANG = f'''SELECT {User_lang} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

SET_WALLET_BALANCE = f'''UPDATE {USR_TBL_NAME} SET {Wallet_balance} = {Wallet_balance} + {val} WHERE {User_id} = {val}'''
GET_WALLET_BALANCE = f'''SELECT {Wallet_balance} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

SET_WALLET_TOTAL = f'''UPDATE {USR_TBL_NAME} SET {Wallet_total} = {Wallet_total} + {val} WHERE {User_id} = {val}'''
GET_WALLET_TOTAL = f'''SELECT {Wallet_total} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

SET_WALLET_RETURN = f'''UPDATE {USR_TBL_NAME} SET {Wallet_return} = {Wallet_return} + {val} WHERE {User_id} = {val}'''
GET_WALLET_RETURN = f'''SELECT {Wallet_return} FROM {USR_TBL_NAME} WHERE {User_id} = {val}'''

'''
функции
'''


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def create_connection():
    connection = None
    try:
        if cnfg.DEBUG:
            connection = sqlite3_connect(f'{DB_NAME}.db')
            print("Connection to SQLite DB successful")
        else:
            connection = pymysql_connect(host=MYSQL_DB_HOST, user=MYSQL_DB_USER,
                                         password=MYSQL_DB_PASSWORD, database=DB_NAME, charset='utf8', autocommit=True)
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def create_database(query, table_name):
    try:
        CURSOR.execute(query)
        print(f"Database {table_name} created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def is_empty_db(connection):
    cursor = connection.cursor()
    cursor.execute(f'SELECT * FROM {USR_TBL_NAME}')
    elems = cursor.fetchall()
    if len(elems) > 0:
        return False
    else:
        return True


def write_data_to_db(connection, query, vars_):
    if cnfg.DEBUG:  # SQLite (локальная)
        with connection as con:
            cursor = connection.cursor()
            if vars_ is None:
                cursor.execute(query)
            else:
                cursor.execute(query, vars_)
            con.commit()
            return cursor
    else:
        while True:  # it works until the data was not saved
            if not connection.open:
                connection.ping(True)
            try:
                cursor = connection.cursor()
                if vars_ is None:
                    cursor.execute(query)
                else:
                    cursor.execute(query, vars_)
                connection.commit()
                return cursor
            except:
                pass


DB_CONNECTION = None
CURSOR = None


def connect():
    global DB_CONNECTION, CURSOR
    DB_CONNECTION = create_connection()
    DB_CONNECTION.row_factory = dict_factory
    CURSOR = DB_CONNECTION.cursor()


connect()
create_database(USERS_TABLE, USR_TBL_NAME)

'''
запросы из базы
'''


def get_user(user_id):
    try:
        query = GET_USER
        cur = write_data_to_db(DB_CONNECTION, query, (user_id,))
        user_id = cur.fetchall()[0]
        if cnfg.DEBUG:
            return user_id[User_id]
        else:
            return user_id[0]
    except:
        return None


def get_id_all_users():
    try:
        query = GET_ID_ALL_USERS
        cur = write_data_to_db(DB_CONNECTION, query, None)
        users_list = cur.fetchall()
        users = []
        for user in users_list:
            if cnfg.DEBUG:
                users.append(user[User_id])
            else:
                users.append(user)[0]
        return users
    except Exception as e:
        return None


def get_id_all_referals(user_id):
    try:
        query = GET_IDS_REFERALS
        cur = write_data_to_db(DB_CONNECTION, query, (user_id,))
        referals_list = cur.fetchall()
        referals = []
        for referal in referals_list:
            if cnfg.DEBUG:
                referals.append(referal[User_id])
            else:
                referals.append(referal)[0]
        return referals
    except Exception as e:
        return None


def SET_user_referer(user_id, user_email):
    write_data_to_db(DB_CONNECTION, SET_USER_REFERER, (user_id, user_email))


def update_id_user_email(user_id, user_email):
    write_data_to_db(DB_CONNECTION, UPDATE_ID_USER_EMAIL, (user_id, user_email))


def update_id_user_phone(user_id, user_phone):
    write_data_to_db(DB_CONNECTION, UPDATE_ID_USER_PHONE, (user_id, user_phone))


def check_email_user(user_email):
    try:
        cur = write_data_to_db(DB_CONNECTION, CHECK_EMAIL_USER, (user_email,))
        user_id = cur.fetchall()[0]
        if cnfg.DEBUG:
            return user_id[User_email]
        else:
            return user_id[0]
    except:
        return None


def check_phone_user(user_phone):
    try:
        cur = write_data_to_db(DB_CONNECTION, CHECK_PHONE_USER, (user_phone,))
        user_id = cur.fetchall()[0]
        if cnfg.DEBUG:
            return user_id[User_phone]
        else:
            return user_id[0]
    except:
        return None


def delete_user(user_email):
    write_data_to_db(DB_CONNECTION, DELETE_USER, (user_email,))


def SET_user_data(mode, user_id, val):
    if mode == 'ID':
        query = SET_NEW_USER
    elif mode == 'email':
        query = SET_USER_EMAIL
    elif mode == 'phone':
        query = SET_USER_PHONE
    elif mode == 'password':
        query = SET_USER_PASSWORD
    elif mode == 'referer':
        query = SET_USER_REFERER
    elif mode == 'lang':
        query = SET_USER_LANG
    elif mode == 'balance':
        query = SET_WALLET_BALANCE
    elif mode == 'return':
        query = SET_WALLET_RETURN
    try:
        write_data_to_db(DB_CONNECTION, query, (val, user_id))
        if mode == 'balance' and int(val) > 0:
            write_data_to_db(DB_CONNECTION, SET_WALLET_TOTAL, (val, user_id))
    except Error as e:
        print(f'Ошибка записи в базу SET_user_data {e}')


def GET_user_data(mode, user_id):
    if mode == 'ID':
        query = GET_USER
        data_addr = User_id if cnfg.DEBUG else 0
    elif mode == 'email':
        query = GET_USER_EMAIL
        data_addr = User_email if cnfg.DEBUG else 1
    elif mode == 'phone':
        query = GET_USER_PHONE
        data_addr = User_phone if cnfg.DEBUG else 3
    elif mode == 'password_email':
        query = GET_USER_PASSWORD_EMAIL
        data_addr = User_password if cnfg.DEBUG else 4
    elif mode == 'password_phone':
        query = GET_USER_PASSWORD_PHONE
        data_addr = User_password if cnfg.DEBUG else 4
    elif mode == 'referer':
        query = GET_USER_REFERER
        data_addr = User_referer if cnfg.DEBUG else 5
    elif mode == 'lang':
        query = GET_USER_LANG
        data_addr = User_lang if cnfg.DEBUG else 6
    elif mode == 'balance':
        query = GET_WALLET_BALANCE
        data_addr = Wallet_balance if cnfg.DEBUG else 7
    elif mode == 'return':
        query = GET_WALLET_RETURN
        data_addr = Wallet_return if cnfg.DEBUG else 9
    elif mode == 'count':
        query = GET_COUNT_REFERALS
        data_addr = mode if cnfg.DEBUG else 0
    try:
        cur = write_data_to_db(DB_CONNECTION, query, (user_id,))
        data = cur.fetchall()[0]
        if mode == 'balance':
            cur = write_data_to_db(DB_CONNECTION, GET_WALLET_TOTAL, (user_id,))
            data1 = cur.fetchall()[0]
            return data[data_addr], data1[Wallet_total]
        if data[data_addr] == '':
            return None
        else:
            return data[data_addr]
    except Exception as e:
        # print(f'Ошибка чтения из базы GET_user_data {e} mode = {mode}')
        return None
