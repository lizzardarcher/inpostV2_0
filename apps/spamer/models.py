# import asyncio
# from asyncio import run

from django.core import validators
from django.db import models
from django.contrib.auth.models import User

# from pyrogram import Client as PyrogramClient

LOG_LEVEL = (
    ('Trace', 'Trace'),
    ('Debug', 'Debug'),
    ('Info', 'Info'),
    ('Warning', 'Warning'),
    ('Fatal', 'Fatal'),
)


class AutoAnsweringTemplate(models.Model):
    text = models.TextField(null=False, blank=False, verbose_name='Text')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Текст автоответчика'
        verbose_name_plural = 'Текст автоответчика'


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    id_account = models.IntegerField(primary_key=True, verbose_name='Account ID')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    api_id = models.IntegerField(null=True, blank=True, verbose_name='API ID')
    api_hash = models.CharField(max_length=100, null=True, blank=True, verbose_name='API HASH')
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон')
    sms_code = models.CharField(default='', max_length=16, null=True, blank=True, verbose_name='SMS код')
    signed_in = models.BooleanField(default=False, blank=True, verbose_name='Активирован')

    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Name')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Surname')
    photo = models.ImageField(null=True, blank=True, verbose_name='Photo')

    status = models.BooleanField(default=True, verbose_name='Состояние')
    is_activated = models.BooleanField(default=False, null=True, blank=True, verbose_name='Активирован')
    is_change_needed = models.BooleanField(default=False, null=True, blank=True, verbose_name='Обновление BIO')
    report = models.TextField(max_length=1000000, null=True, blank=True, verbose_name='Отчёт о состоянии')
    session = models.FileField(upload_to='sessions', max_length=1000, null=True, blank=False, verbose_name='Сессия',
                               validators=[validators.FileExtensionValidator(['session'])])
    session_for_chat = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Сессия для чатов')
    session_for_lk = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Сессия для лс')

    common_text = models.TextField(max_length=4000, null=True, blank=True, verbose_name='Текст Рассылки')
    media = models.FileField(null=True, blank=True, verbose_name='Image')
    auto_answering_text = models.TextField(max_length=4000, null=True, blank=True, verbose_name='Текст автоответчика')
    auto_answering_text_ref = models.ForeignKey(AutoAnsweringTemplate, on_delete=models.CASCADE, related_name='autoref',
                                                default=None, null=True, blank=True, verbose_name='Текст автоответчика')

    is_auto_answering_active = models.BooleanField(default=False, null=True, blank=True,
                                                   verbose_name='Автоответчик вкл/выкл')
    is_spam_active = models.BooleanField(default=False, null=True, blank=True, verbose_name='Спам вкл/выкл')
    is_spam_lk_active = models.BooleanField(default=False, null=True, blank=True, verbose_name='Спам по ЛС вкл/выкл')
    delay = models.IntegerField(default=5, null=True, blank=True,
                                verbose_name='Задержка отправки сообщения (в минутах)')
    master_to_forward = models.CharField(max_length=100, null=True, blank=True,
                                         verbose_name='Кому пересылать сообщения')
    account_enabled = models.BooleanField(default=True, null=True, blank=True, verbose_name='Задействован в чатах')

    def __str__(self):
        if self.status:
            return '✅ ' + str(self.first_name)
            # return '✅ @' + str(self.username).split('/')[-1]
        else:
            return '❌ ' + str(self.first_name)
            # return '❌ @' + str(self.username).split('/')[-1]

    class Meta:
        db_table = 'account'
        verbose_name = 'Спам Аккаунт'
        verbose_name_plural = 'Спам Аккаунты'


class Message(models.Model):
    id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='ID')
    message_id = models.IntegerField(default=None, null=True, blank=True, verbose_name='ID сообщения')
    account = models.ForeignKey(to='Account', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Аккаунт')
    chat = models.ForeignKey(to='Chat', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Чат')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    is_deleted = models.BooleanField(default=False, null=True, blank=True, verbose_name='Удалено из группы')

    def __str__(self):
        return str(self.message_id) + ' ' + str(self.account)

    class Meta:
        db_table = 'message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spamchat', null=True, blank=True,
                             verbose_name='Пользователь')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    image = models.ImageField(null=True, blank=True, verbose_name='Image')
    data_image = models.CharField(max_length=4000, null=True, blank=True, verbose_name='Data Image')
    link = models.URLField(null=True, blank=True, verbose_name='Link')
    title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Название чата')
    subscribers = models.IntegerField(default=0, null=True, blank=True, verbose_name='Подписчиков')
    username = models.CharField(max_length=1000, unique=True, null=True, blank=True, verbose_name='Ссылка или Юзернейм')
    text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Текст для чата')
    delay = models.IntegerField(default=0, null=True, blank=True, verbose_name='Задержка (мин)')
    is_user_banned = models.ManyToManyField(to='Account', null=True, blank=True, verbose_name='Бан')
    is_emoji_allowed = models.BooleanField(default=True, null=True, blank=True, verbose_name='Emoji')
    is_del_mes_available = models.BooleanField(default=True, null=True, blank=True, verbose_name='Del msg')
    is_active = models.BooleanField(default=True, null=True, blank=True, verbose_name='Чат активен')
    comment = models.TextField(max_length=1024, default='', null=True, blank=True, verbose_name='Комментарий')
    worked_out = models.BooleanField(default=False, null=True, blank=True, verbose_name='Отработан')

    def __str__(self):
        return str(self.title).upper()

    class Meta:
        db_table = 'chat'
        verbose_name = 'Группа для Спама'
        verbose_name_plural = 'Группы для Спама'
        unique_together = (('user', 'link'),)


class ChannelToSubscribe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spamchannel', null=True, blank=True,
                             verbose_name='Пользователь')
    username = models.CharField(max_length=1000, unique=True, null=True, blank=True, verbose_name='Username')

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = 'channel_to_subscribe'
        verbose_name = 'Канал для подписки'
        verbose_name_plural = 'Каналы для подписки'


class ChatMaster(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='Chat Id')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    title = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Название чата')
    comment = models.CharField(max_length=1000, null=True, blank=True, verbose_name='#')

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = 'chatmaster'
        verbose_name = 'Чат с мастер аккаунтом'
        verbose_name_plural = 'Чаты с мастер аккаунтом'


class Client(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    user_id = models.IntegerField(null=True, blank=True, verbose_name='User_id')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    first_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Фамилия')
    last_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Имя')
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Телефон')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='spmacc', null=True, blank=True,
                                verbose_name='Account')

    def __str__(self):
        return '@' + str(self.username) + ' ' + str(self.user_id)

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = (('user_id', 'account'),)


class MasterAccount(models.Model):
    id_account = models.IntegerField(primary_key=True, verbose_name='Account ID')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='Username')
    api_id = models.IntegerField(null=True, blank=True, verbose_name='API ID')
    api_hash = models.CharField(max_length=100, null=True, blank=True, verbose_name='API HASH')
    phone = models.CharField(max_length=16, null=True, blank=True, verbose_name='Phone')
    status = models.BooleanField(default=True, verbose_name='Состояние')
    report = models.TextField(max_length=1000000, null=True, blank=True, verbose_name='Отчёт о состоянии')
    session = models.CharField(max_length=100, null=True, blank=True, verbose_name='Сессия')
    is_master = models.BooleanField(default=False, null=True, blank=True, verbose_name='Мастер')
    is_duplicate = models.BooleanField(default=False, null=True, blank=True, verbose_name='Дубликат')

    def __str__(self):
        return '@' + str(self.username).split('/')[-1] + ' ' + str(self.id_account)

    class Meta:
        db_table = 'masteraccount'
        verbose_name = 'Мастер аккаунт'
        verbose_name_plural = 'Мастер Аккаунты'


class GeneralLogging(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spamlog', null=True, blank=True,
                             verbose_name='Пользователь')
    log_level = models.CharField(max_length=50, null=True, blank=True, choices=LOG_LEVEL,
                                 verbose_name='Уровень логгирования')
    message = models.TextField(max_length=4000, null=True, blank=True, verbose_name='Сообщение')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    account = models.ForeignKey(to='Account', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Аккаунт')
    chat = models.ForeignKey(to='Chat', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Чат')

    class Meta:
        db_table = 'commonlogging'
        verbose_name = 'Лог общий'
        verbose_name_plural = 'Логи общие'


class AccountLogging(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spamlogging', null=True, blank=True,
                             verbose_name='Пользователь')
    log_level = models.CharField(max_length=50, null=True, blank=True, choices=LOG_LEVEL,
                                 verbose_name='Уровень логгирования')
    message = models.TextField(max_length=4000, null=True, blank=True, verbose_name='Сообщение')
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    account = models.ForeignKey(to='Account', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Аккаунт')
    chat = models.ForeignKey(to='Chat', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Чат')
    client = models.ForeignKey(to='Client', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='Клиент')

    class Meta:
        db_table = 'accountlogging'
        verbose_name = 'Лог аккаунта'
        verbose_name_plural = 'Логи аккаунтов'


class Bot(models.Model):
    token = models.CharField(null=False, blank=False, max_length=1000, verbose_name='Bot Token (‼️ не трогать ‼️)')
    link = models.CharField(null=False, blank=False, max_length=1000, verbose_name='Ссылка на бота (‼️ не трогать ‼️)')

    def __str__(self):
        return self.link + '   ||   ' + self.token

    class Meta:
        verbose_name = 'Бот'
        verbose_name_plural = 'Бот'


class TGAdmin(models.Model):
    user_id = models.IntegerField(primary_key=True, verbose_name='User ID')
    username = models.CharField(max_length=100, null=True, blank=True, verbose_name='User Name')

    def __str__(self):
        return str(self.username) + ' ' + str(self.user_id)

    class Meta:
        verbose_name = 'Админ'
        verbose_name_plural = 'Админы'


class GeneralSettings(models.Model):
    is_reload_spam_needed = models.BooleanField(default=False, null=True, blank=True,
                                                verbose_name='Нужна ли перезагрузка спамера')

    # forward_lk = models.CharField(max_length=100, null=True, blank=True, verbose_name='Пересыл в ЛС')
    # general_text = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Общий Текст')
    # general_auto_answering = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Общий автоответчик')
    # general_delay = models.IntegerField(default=0, null=True, blank=True,
    #                                     verbose_name='Общая задержка отправки сообщения (в минутах)')

    def __str__(self):
        return 'Общие настройки для всего бота'

    class Meta:
        verbose_name = 'Общие настройки'
        verbose_name_plural = 'Общие настройки'
