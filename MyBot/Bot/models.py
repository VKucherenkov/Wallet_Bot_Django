from django.db import models
from django.urls import reverse


# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOISES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    telegram_id = models.PositiveBigIntegerField(('ID Telegram'), null=True, db_index=True, unique=True)
    email = models.EmailField(('email'), blank=True, null=True)
    first_name = models.CharField(('Имя'), max_length=20, blank=True, null=True)
    last_name = models.CharField(('Фамилия'), max_length=20, blank=True, null=True)
    gender = models.CharField(('Пол'), max_length=1, choices=GENDER_CHOISES, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время регистрации'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последней активности'), auto_now=True, blank=True, null=True)

    def get_url(self):
        return reverse('user-detail', args=[self.id])

    def __str__(self):
        return (f'id = {self.telegram_id} ---- '
                f'имя = {self.first_name}')

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
        return (f'Имя банка = {self.name_bank}')


class CardUser(models.Model):
    '''Карты пользователя'''
    TelegramUser_CardUser = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='cards')
    BankCard_CardUser = models.ForeignKey(BankCard, on_delete=models.CASCADE, related_name='cards')
    name_card = models.CharField(('Имя карты'), max_length=150, blank=True, null=True)
    number_card = models.IntegerField(('Номер карты'), null=True, unique=True)
    balans_card = models.DecimalField('Баланс карты', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                      null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Платежная карта'
        verbose_name_plural = 'Платежные карты'

    def __str__(self):
        return (f'\nимя = {self.name_card}, номер карты: {self.number_card},\n'
                f'Баланс карты: {self.balans_card},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время последнего изменения: {self.datetime_update},\n'
                f'Владелец: {self.TelegramUser_CardUser.first_name}\n'
                )


class TypeOperation(models.Model):
    '''Тип операции'''
    name_type = models.CharField(('Наименование типа'), max_length=150, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def __str__(self):
        return (f'\nТип операции = {self.name_type},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )


class CategoryOperation(models.Model):
    '''Категория операции'''
    TypeOperation_CategoryOperation = models.ForeignKey(TypeOperation, on_delete=models.CASCADE,
                                                        related_name='typeoperation')
    name_cat = models.CharField(('Наименование категории'), max_length=150, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Категория операции'
        verbose_name_plural = 'Категории операций'

    def __str__(self):
        return (f'\nКатегория = {self.name_cat},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )


class OperationUser(models.Model):
    '''Операция списания/зачисления'''
    CardUser_OperationUser = models.ForeignKey(CardUser, on_delete=models.CASCADE, related_name='Operation')
    CategoryOperation_OperationUser = models.ForeignKey(CategoryOperation, on_delete=models.CASCADE,
                                                        related_name='Operation')
    datetime_amount = models.DateTimeField(('Время операции'), blank=True, null=True)
    amount_operation = models.DecimalField('Сумма операции', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                           null=True)
    note_operation = models.CharField(('Текст уведомления'), max_length=250, blank=True, null=True)
    datetime_add = models.DateTimeField(('Время добавления'), auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'), auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Операция списания/зачисления'
        verbose_name_plural = 'Операции списаний/зачислений'

    def __str__(self):
        return (f'\nСумма операции = {self.amount_operation},\n'
                f'Время операции = {self.datetime_amount},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )


class Recipient(models.Model):
    '''Получатели/плательщики'''
    categories = models.ManyToManyField(CategoryOperation, through='Cat_Recipient')
    name_recipient = models.CharField(('Наименование контрагента'),
                                      max_length=150,
                                      blank=True, null=True)
    recipient_in_notification = models.CharField(('Контрагент в уведомлении'),
                                                 max_length=150,
                                                 blank=True,
                                                 null=True)
    datetime_add = models.DateTimeField(('Время добавления'),
                                        auto_now_add=True,
                                        blank=True,
                                        null=True)
    datetime_update = models.DateTimeField(('Время последнего изменения'),
                                           auto_now=True,
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'Получатель/плательщик'
        verbose_name_plural = 'Получатели/плательщики'

    def __str__(self):
        return (f'\nНаименование контрагента = {self.name_recipient},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )


class Cat_Recipient(models.Model):
    category = models.ForeignKey(CategoryOperation, on_delete=models.CASCADE)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    datetime_add = models.DateTimeField(('Время создания'),
                                        auto_now_add=True,
                                        blank=True,
                                        null=True)
    datetime_update = models.DateTimeField(('Время последнего использования'),
                                           auto_now=True,
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'Получатель - Категория'
        verbose_name_plural = 'Получатели - Категории'

    def __str__(self):
        return (f'\nНаименование контрагента = {self.recipient.name_recipient},\n'
                f'Наименование категории = {self.category.name_cat},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )
