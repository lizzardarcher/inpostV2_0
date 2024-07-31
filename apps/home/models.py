# -*- encoding: utf-8 -*-
from datetime import datetime

import django
from django.db import models
from django.contrib.auth.models import User
from markitup.fields import MarkupField
from django.utils.timezone import now
from . import validators

tz_choice = [
    # ('(UTC-12:00) International Date Line West', ),
    # ('(UTC-11:00) Coordinated Universal Time-11', ),
    # ('(UTC-10:00) Hawaii', ),
    # ('(UTC-09:00) Alaska', ),
    # ('(UTC-08:00) Baja California', ),
    # ('(UTC-08:00) Pacific Time (US & Canada)', ),
    # ('(UTC-07:00) Arizona', ),
    # ('(UTC-07:00) Chihuahua, La Paz, Mazatlan', ),
    # ('(UTC-07:00) Mountain Time (US & Canada)', ),
    # ('(UTC-06:00) Central America', ),
    # ('(UTC-06:00) Central Time (US & Canada)', ),
    # ('(UTC-06:00) Guadalajara, Mexico City, Monterrey', ),
    # ('(UTC-06:00) Saskatchewan', ),
    # ('(UTC-05:00) Bogota, Lima, Quito', ),
    # ('(UTC-05:00) Eastern Time (US & Canada)', ),
    # ('(UTC-05:00) Indiana (East)', ),
    # ('(UTC-04:30) Caracas', ),
    # ('(UTC-04:00) Asuncion', ),
    # ('(UTC-04:00) Atlantic Time (Canada)', ),
    # ('(UTC-04:00) Cuiaba', ),
    # ('(UTC-04:00) Georgetown, La Paz, Manaus, San Juan', ),
    # ('(UTC-04:00) Santiago', ),
    # ('(UTC-03:30) Newfoundland', ),
    # ('(UTC-03:00) Brasilia', ),
    # ('(UTC-03:00) Buenos Aires', ),
    # ('(UTC-03:00) Cayenne, Fortaleza', ),
    # ('(UTC-03:00) Greenland', ),
    # ('(UTC-03:00) Montevideo', ),
    # ('(UTC-03:00) Salvador', ),
    # ('(UTC-02:00) Coordinated Universal Time-02', ),
    # ('(UTC-02:00) Mid-Atlantic - Old', ),
    # ('(UTC-01:00) Azores', ),
    # ('(UTC-01:00) Cape Verde Is.', ),
    # ('(UTC) Casablanca', ),
    # ('(UTC) Coordinated Universal Time', ),
    # ('(UTC) Dublin, Edinburgh, Lisbon, London', ),
    # ('(UTC) Monrovia, Reykjavik', ),
    # ('(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna', ),
    # ('(UTC+01:00) Belgrade, Bratislava, Budapest, Ljubljana, Prague', ),
    # ('(UTC+01:00) Brussels, Copenhagen, Madrid, Paris', ),
    # ('(UTC+01:00) Sarajevo, Skopje, Warsaw, Zagreb', ),
    # ('(UTC+01:00) West Central Africa', ),
    # ('(UTC+01:00) Windhoek', ),
    # ('(UTC+02:00) Athens, Bucharest', ),
    # ('(UTC+02:00) Beirut', ),
    # ('(UTC+02:00) Cairo', ),
    # ('(UTC+02:00) Damascus', ),
    # ('(UTC+02:00) E. Europe', ),
    # ('(UTC+02:00) Harare, Pretoria', ),
    # ('(UTC+02:00) Helsinki, Kyiv, Riga, Sofia, Tallinn, Vilnius', ),
    # ('(UTC+02:00) Istanbul', ),
    # ('(UTC+02:00) Jerusalem', ),
    # ('(UTC+02:00) Tripoli', ),
    # ('(UTC+03:00) Amman', ),
    # ('(UTC+03:00) Baghdad', ),
    # ('(UTC+03:00) Kaliningrad, Minsk', ),
    # ('(UTC+03:00) Kuwait, Riyadh', ),
    # ('(UTC+03:00) Nairobi', ),
    # ('(UTC+03:30) Tehran', ),
    # ('(UTC+04:00) Abu Dhabi, Muscat', ),
    # ('(UTC+04:00) Baku', ),
    ('+4 Москва', 'Москва'),
    ('+4 СПб', 'СПб'),
    # ('(UTC+04:00) Port Louis', ),
    # ('(UTC+04:00) Tbilisi', ),
    # ('(UTC+04:00) Yerevan', ),
    # ('(UTC+04:30) Kabul', ),
    # ('(UTC+05:00) Ashgabat, Tashkent', ),
    # ('(UTC+05:00) Islamabad, Karachi', ),
    # ('(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi', ),
    # ('(UTC+05:30) Sri Jayawardenepura', ),
    # ('(UTC+05:45) Kathmandu', ),
    # ('(UTC+06:00) Astana', ),
    # ('(UTC+06:00) Dhaka', ),
    ('+6 Екатеринбург', 'Екатеринбург'),
    # ('(UTC+06:30) Yangon (Rangoon)', ),
    # ('(UTC+07:00) Bangkok, Hanoi, Jakarta', ),
    # ('(UTC+07:00) Novosibirsk', ),
    # ('(UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi', ),
    # ('(UTC+08:00) Krasnoyarsk', ),
    # ('(UTC+08:00) Kuala Lumpur, Singapore', ),
    # ('(UTC+08:00) Perth', ),
    # ('(UTC+08:00) Taipei', ),
    # ('(UTC+08:00) Ulaanbaatar', ),
    # ('(UTC+09:00) Irkutsk', ),
    # ('(UTC+09:00) Osaka, Sapporo, Tokyo', ),
    # ('(UTC+09:00) Seoul', ),
    # ('(UTC+09:30) Adelaide', ),
    # ('(UTC+09:30) Darwin', ),
    # ('(UTC+10:00) Brisbane', ),
    # ('(UTC+10:00) Canberra, Melbourne, Sydney', ),
    # ('(UTC+10:00) Guam, Port Moresby', ),
    # ('(UTC+10:00) Hobart', ),
    # ('(UTC+10:00) Yakutsk', ),
    # ('(UTC+11:00) Solomon Is., New Caledonia', ),
    # ('(UTC+11:00) Vladivostok', ),
    # ('(UTC+12:00) Auckland, Wellington', ),
    # ('(UTC+12:00) Coordinated Universal Time+12', ),
    # ('(UTC+12:00) Fiji', ),
    # ('(UTC+12:00) Magadan', ),
    # ('(UTC+12:00) Petropavlovsk-Kamchatsky - Old', ),
    # ('(UTC+13:00) Samoa', ),
]


class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post_sent = models.IntegerField(default=0, null=True, blank=True, verbose_name='Отправлено всего постов')
    send_errors = models.IntegerField(default=0, null=True, blank=True, verbose_name='Ошибок отправки постов')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Статистика'
        verbose_name_plural = 'Статистика'


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    exp_date = models.DateField(default=django.utils.timezone.now, null=True, blank=True, verbose_name='Оплачено по:')
    is_vip = models.BooleanField(default=False, blank=True, verbose_name='VIP')
    primary_color = models.CharField(max_length=100,
                                     choices=[('primary', 'Розовый'), ('blue', 'Синий'), ('orange', 'Оранжевый'),
                                              ('red', 'Красный'), ('green', 'Зеленый')],
                                     default='Розовый', blank=True, verbose_name='Основной цвет')
    main_theme = models.CharField(max_length=100, choices=[('white-content', 'Светлая'), ('', 'Темная')],
                                  default='Темная',
                                  blank=True, verbose_name='Тема Оформления')
    tz = models.CharField(max_length=100, blank=True, default='Москва', choices=tz_choice, verbose_name='Город')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Статус оплаты'
        verbose_name_plural = 'Статус оплаты'


class Bot(models.Model):
    ref = models.CharField(max_length=100, verbose_name='Ссылка на бота', validators=[validators.validate_post_name])
    token = models.CharField(max_length=300, verbose_name='Бот Токен')
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Назавание бота')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.title

    def get_chat_username(self):
        return self.ref.split('/')[0]

    class Meta:
        ordering = ['id']
        verbose_name = "Бот"
        verbose_name_plural = "Боты"


class Template(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    title = models.CharField(max_length=100, null=False, blank=False, verbose_name='Название шаблона')
    text = models.TextField(max_length=10000, null=True, blank=True, verbose_name='Текст')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return 'Шаблон ' + self.title

    class Meta:
        ordering = ['id']
        verbose_name = "Шаблон"
        verbose_name_plural = "Шаблоны"


class Post(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name='Заголовок поста',
                            validators=[validators.validate_post_name])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    post_type = models.CharField(default='Пост', max_length=20, choices=[('Пост', 'Пост'), ('Опрос', 'Опрос')],
                                 null=True, blank=False, verbose_name='Тип поста')
    text = models.TextField(max_length=10000, null=True, blank=True, verbose_name='Текст')
    is_active = models.BooleanField(null=True, blank=True, default=False, verbose_name='Активно')
    template = models.ForeignKey(Template, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Шаблон')

    photo_1 = models.ImageField(max_length=4000, null=True, blank=True, verbose_name='Фото 1')
    photo_2 = models.ImageField(max_length=4000, null=True, blank=True, verbose_name='Фото 2')
    photo_3 = models.ImageField(max_length=4000, null=True, blank=True, verbose_name='Фото 3')
    photo_4 = models.ImageField(max_length=4000, null=True, blank=True, verbose_name='Фото 4')
    photo_5 = models.ImageField(max_length=4000, null=True, blank=True, verbose_name='Фото 5')

    music = models.FileField(max_length=4000, null=True, blank=True, verbose_name='Музыкальный Трек')

    video = models.FileField(max_length=4000, null=True, blank=True, verbose_name='Видео Запись')

    document = models.FileField(max_length=4000, null=True, blank=True, verbose_name='Документ')

    url = models.CharField(max_length=4000, null=True, blank=True, verbose_name='Ссылка',
                           validators=[validators.post_ref_validator])
    url_text = models.CharField(max_length=4000, null=True, blank=True, verbose_name='Текст внутри ссылки')

    btn_name_1 = models.CharField(max_length=100, null=True, blank=True, verbose_name='')
    btn_name_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name='')
    btn_name_3 = models.CharField(max_length=100, null=True, blank=True, verbose_name='')
    btn_name_4 = models.CharField(max_length=100, null=True, blank=True, verbose_name='')

    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=False, verbose_name='Пост')
    schedule = models.DateTimeField(null=True, blank=False, verbose_name='Расписание')
    is_sent = models.BooleanField(default=False, null=True, blank=True, verbose_name='Отправлено')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.schedule) + str(self.is_sent)

    def save(self, *args, **kwargs):
        super(PostSchedule, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = "Расписание"
        verbose_name_plural = "Расписание"


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    photo_1 = models.ImageField(null=True, blank=True, verbose_name='Фото 1')
    photo_2 = models.ImageField(null=True, blank=True, verbose_name='Фото 2')
    photo_3 = models.ImageField(null=True, blank=True, verbose_name='Фото 3')
    photo_4 = models.ImageField(null=True, blank=True, verbose_name='Фото 4')
    photo_5 = models.ImageField(null=True, blank=True, verbose_name='Фото 5')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.post.name + ' - ' + str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = "Фото"
        verbose_name_plural = "Фото"


class PostMusic(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    music = models.FileField(verbose_name='Музыкальный Трек')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.post.name + ' - ' + str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = "Муз Трек"
        verbose_name_plural = "Муз Треки"


class PostVideo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    video = models.FileField(verbose_name='Видео Запись')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.post.name + ' - ' + str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = "Видео Запись"
        verbose_name_plural = "Видео Записи"


class PostDocument(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    document = models.FileField(verbose_name='Документ')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.post.name + ' - ' + str(self.id)

    class Meta:
        ordering = ['id']
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class PostReference(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    reference = models.CharField(max_length=300, null=True, blank=False, verbose_name='Ссылка',
                                 validators=[validators.post_ref_validator])
    text = models.CharField(max_length=300, null=True, blank=False, verbose_name='Текст внутри ссылки')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.post.name + ' - ' + str(self.id) + ' - ' + str(self.reference)

    class Meta:
        ordering = ['id']
        verbose_name = "Ссылка"
        verbose_name_plural = "Ссылки"


class Button(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='')
    rating = models.IntegerField(null=True, blank=True, verbose_name='Рейтинг')
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name + ' --- Пост-' + self.post.name + ' Рейтинг-' + str(self.rating)

    class Meta:
        ordering = ['id']
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"


class Media(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пост')
    media = models.FileField(null=True, blank=True, verbose_name='Медиа файл')
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['id']
        verbose_name = 'Медиа'
        verbose_name_plural = 'Медиа'

    def __str__(self):
        return str(self.media)


class Chat(models.Model):
    chat_type = models.CharField(max_length=20, choices=[('Группа', 'Группа'), ('Канал', 'Канал')], null=True,
                                 blank=False, verbose_name='Тип Чата')
    # name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название')
    ref = models.CharField(max_length=200, null=True, unique=True, validators=[validators.validate_contains_https],
                           verbose_name='Ссылка на чат')
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Название канала')
    image = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Ссылка на изображение канала')
    subscribers = models.IntegerField(null=True, blank=True, verbose_name='Кол-во подписчиков')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    chat_id = models.BigIntegerField(default=0, null=True, blank=True, verbose_name='ID чата')

    positive_subs = models.IntegerField(default=0, null=True, blank=True,
                                        verbose_name='Количество подписавшихся за сутки')
    negative_subs = models.IntegerField(default=0, null=True, blank=True,
                                        verbose_name='Количество отписавшихся за сутки')

    mon_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 1')
    tue_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 2')
    wed_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 3')
    thu_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 4')
    fri_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 5')
    sat_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 6')
    sun_stat_subs = models.IntegerField(default=0, null=True, blank=True, verbose_name='Статистика подписчиков 7')

    id = models.AutoField(primary_key=True, editable=False)
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, null=True, default=None, blank=False, verbose_name='Бот')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['id']

    def __str__(self):
        return self.ref


class Notification(models.Model):
    text = models.CharField(max_length=500, null=True, blank=True, verbose_name='Текст уведомления')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомление'
        ordering = ['-id']

    def __str__(self):
        return self.text
