from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    telegram_id = models.PositiveBigIntegerField(('ID Telegram'), null=True, db_index=True, unique=True)
    email = models.EmailField(('email'), blank=True, null=True)
    first_name = models.CharField(('Имя'), max_length=150, blank=True, null=True)
    last_name = models.CharField(('Фамилия'), max_length=150, blank=True, null=True)
    datetime_join = models.DateTimeField(('Время регистрации'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последней активности'), auto_now=True,blank=True, null=True)

    def __str__(self):
        return f'имя = {self.first_name}, id = {self.telegram_id}\n'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
