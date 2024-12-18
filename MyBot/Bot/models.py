from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    telegram_id = models.PositiveBigIntegerField(('ID Telegram'), null=True, db_index=True, unique=True)
    email = models.EmailField(('email'), blank=True, null=True)
    first_name = models.CharField(('Имя'), max_length=150, blank=True, null=True)
    last_name = models.CharField(('Фамилия'), max_length=150, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время регистрации'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последней активности'), auto_now=True, blank=True, null=True)

    def __str__(self):
        return f'\nимя = {self.first_name},' \
               f'id = {self.telegram_id},\n' \
               f'Регистрация = {self.datetime_add}, ' \
               f'Был = {self.datetime_update}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class BankCard(models.Model):
    '''Банки эмитенты карт'''
    name_bank = models.CharField(('Имя банка'), max_length=150, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Банк эмитент'
        verbose_name_plural = 'Банки эмитенты'

    def __str__(self):
        return (f'\nИмя банка = {self.name_bank},\n'
                f'Время добавления = {self.datetime_add}')

class CardUser(models.Model):
    '''Карты пользователя'''
    TelegramUser_CardUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='cards')
    BankCard_CardUser = models.ForeignKey(BankCard, on_delete=models.CASCADE, related_name='cards')
    title = models.CharField(('Имя карты'), max_length=150, blank=True, null=True)
    number_card = models.IntegerField(('Номер карты'), null=True, unique=True)
    balans_card = models.DecimalField('Баланс карты', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                      null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Платежная карта'
        verbose_name_plural = 'Платежные карты'

    def __str__(self):
        return (f'\nимя = {self.title}, id = {self.number_card},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Владелец: {self.TelegramUser_CardUser.first_name}\n'
                f'Баланс карты: {self.balans_card}')
