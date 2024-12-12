from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    telegram_id = models.PositiveBigIntegerField(('ID Telegram'), null=True, db_index=True, unique=True)
    username = models.CharField(('Юзернейм'), max_length=150, blank=True, null=True)
    email = models.EmailField(('email'), blank=True, null=True)
    first_name = models.CharField(('Имя'), max_length=150, blank=True, null=True)
    last_name = models.CharField(('Фамилия'), max_length=150, blank=True, null=True)
    datetime_join = models.DateTimeField(('Время регистрации'), blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последней активности'), blank=True, null=True)


    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
