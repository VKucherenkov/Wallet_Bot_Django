from django.db import models

# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    telegram_id = models.PositiveBigIntegerField(('ID Telegram'), null=True, db_index=True, unique=True)
    email = models.EmailField(('email'), blank=True, null=True)
    first_name = models.CharField(('Имя'), max_length=150, blank=True, null=True)
    last_name = models.CharField(('Фамилия'), max_length=150, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время регистрации'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последней активности'), auto_now=True,blank=True, null=True)

    def __str__(self):
        return f'\nимя = {self.first_name}, id = {self.telegram_id},\nРегистрация = {self.datetime_join}, Был = {self.datetime_update}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'

class CardUser(models.Model):
    TelegramUser_CardUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(('Имя карты'), max_length=150, blank=True, null=True)
    number_card = models.IntegerField(('Номер карты'), null=True, unique=True)
    balans_card = models.DecimalField('Баланс карты', max_digits=10, decimal_places=2, db_index=True, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True,blank=True, null=True)

    class Meta:
        verbose_name = 'Платежная карта'
        verbose_name_plural = 'Платежные карты'

    def __str__(self):
        return (f'\nимя = {self.title}, id = {self.number_card},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Владелец: {self.TelegramUser_CardUser.first_name}\n'
                f'Баланс карты: {self.balans_card}')
