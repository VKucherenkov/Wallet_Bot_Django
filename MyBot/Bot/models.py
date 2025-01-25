from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


# Расширяем модель User
class MyUser(AbstractUser):
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]
    # Добавляем дополнительные поля
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True,
                              verbose_name="Пол")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    slug = AutoSlugField(populate_from='username', max_length=255, unique=True, db_index=True, verbose_name="slug")

    def get_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})

    def __str__(self):
        return self.username

# Create your models here.
class TelegramUser(models.Model):
    '''Пользователи чат бота'''
    MALE = 'M'
    FEMALE = 'Ж'
    GENDER_CHOICES = [
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина')
    ]

    telegram_id = models.PositiveBigIntegerField('ID Telegram', null=True, db_index=True, unique=True)
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=20, blank=True, null=True, verbose_name="Фамилия")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True,
                              verbose_name="Пол")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    slug = AutoSlugField(populate_from='telegram_id', max_length=255, unique=True, db_index=True, verbose_name="slug")
    datetime_add = models.DateTimeField('Время регистрации', auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField('Время последней активности', auto_now=True, blank=True, null=True)

    def get_url(self):
        return reverse('userdetail', kwargs={'userdetail_slug': self.slug})

    def __str__(self):
        return (f'id: {self.telegram_id} ---- '
                f'имя: {self.first_name}')

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class BankCard(models.Model):
    '''Банки эмитенты карт'''
    name_bank = models.CharField(max_length=150, blank=True, null=True, verbose_name='Банк')
    slug = AutoSlugField(populate_from='name_bank', max_length=255, unique=True, db_index=True, verbose_name="slug")
    datetime_add = models.DateTimeField('Время добавления', auto_now_add=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Банк эмитент'
        verbose_name_plural = 'Банки эмитенты'

    def get_url(self):
        return reverse('bank-detail', args=[self.slug])

    def __str__(self):
        return f'{self.name_bank}'


class CardUser(models.Model):
    '''Карты пользователя'''
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='cards_user',
                                      verbose_name="Пользователь")
    bank = models.ForeignKey(BankCard, on_delete=models.CASCADE, related_name='cards_bank', verbose_name="Банк")
    name_card = models.CharField(max_length=150, blank=True, null=True,
                                 verbose_name="Наименование карты")
    number_card = models.IntegerField('Номер карты', null=True, unique=True)
    balans_card = models.DecimalField('Баланс карты', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                      null=True)
    datetime_add = models.DateTimeField('Время добавления', auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField('Время последнего изменения', auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Платежная карта'
        verbose_name_plural = 'Платежные карты'

    def get_url(self):
        return reverse('card-detail', args=[self.id])

    def __str__(self):
        return (f'номер карты: {self.number_card}, {self.name_card.upper()}')


class TypeOperation(models.Model):
    '''Тип операции'''
    name_type = models.CharField(max_length=150, blank=True, null=True, verbose_name='Наименование типа')
    slug = AutoSlugField(populate_from='name_type', max_length=255, unique=True, db_index=True, verbose_name="slug")
    datetime_add = models.DateTimeField('Время добавления', auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField('Время последнего изменения', auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Тип операции'
        verbose_name_plural = 'Типы операций'

    def get_url(self):
        return reverse('type-detail', args=[self.slug])

    def __str__(self):
        return f'Тип операции: {self.name_type}'


class CategoryOperation(models.Model):
    '''Категория операции'''
    type = models.ForeignKey(TypeOperation, on_delete=models.CASCADE,
                             related_name='typeoperation', verbose_name='Тип операции')
    name_cat = models.CharField(max_length=150, blank=True, null=True, verbose_name='Наименование категории')
    slug = AutoSlugField(populate_from='name_cat', max_length=255, unique=True, db_index=True, verbose_name="slug")
    datetime_add = models.DateTimeField('Время добавления', auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField('Время последнего изменения', auto_now=True, blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'Категория операции'
        verbose_name_plural = 'Категории операций'

    def get_url(self):
        return reverse('category-detail', args=[self.slug])

    def __str__(self):
        return (f'Категория: {self.name_cat},  '
                f'{self.type}')


class OperationUser(models.Model):
    '''Операция списания/зачисления'''
    card = models.ForeignKey(CardUser, on_delete=models.CASCADE, related_name='Operation',
                             verbose_name='Карта')
    category = models.ForeignKey(CategoryOperation, on_delete=models.CASCADE,
                                 related_name='Operation', verbose_name="Категория")
    datetime_amount = models.DateTimeField('Время операции', blank=True, null=True)
    amount_operation = models.DecimalField('Сумма операции', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                           null=True)
    note_operation = models.CharField(max_length=250, blank=True, null=True, verbose_name='Текст уведомления')
    balans = models.DecimalField('Баланс после операции', max_digits=10, decimal_places=2, db_index=True, blank=True,
                                      null=True)
    datetime_add = models.DateTimeField('Время добавления', auto_now_add=True, blank=True, null=True)
    datetime_update = models.DateTimeField('Время последнего изменения', auto_now=True, blank=True, null=True)

    class Meta:
        verbose_name = 'Операция списания/зачисления'
        verbose_name_plural = 'Операции списаний/зачислений'

    def get_url(self):
        return reverse('operation-detail', args=[self.id])

    def __str__(self):
        return (f'\nСумма операции = {self.amount_operation},\n'
                f'Время операции = {self.datetime_amount},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )


class Recipient(models.Model):
    '''Получатели/плательщики'''
    categories = models.ManyToManyField(CategoryOperation, through='Cat_Recipient')
    name_recipient = models.CharField(max_length=150, blank=True, null=True, verbose_name='Получатель платежа')
    recipient_in_notification = models.CharField(max_length=150, blank=True, null=True,
                                                 verbose_name="Получатель в уведомлении")
    slug = AutoSlugField(populate_from='name_recipient', max_length=255, unique=True, db_index=True, verbose_name="slug")
    datetime_add = models.DateTimeField('Время добавления',
                                        auto_now_add=True,
                                        blank=True,
                                        null=True)
    datetime_update = models.DateTimeField('Время последнего изменения',
                                           auto_now=True,
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'Получатель/плательщик'
        verbose_name_plural = 'Получатели/плательщики'

    def get_url(self):
        return reverse('recipient-detail', args=[self.slug])

    def __str__(self):
        return f'Наименование контрагента: {self.name_recipient}'


class Cat_Recipient(models.Model):
    category = models.ForeignKey(CategoryOperation, on_delete=models.CASCADE, related_name='recipient_cat', verbose_name="Категория")
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, related_name='categories_recepient', verbose_name="Получатель платежа")
    datetime_add = models.DateTimeField('Время создания',
                                        auto_now_add=True,
                                        blank=True,
                                        null=True)
    datetime_update = models.DateTimeField('Время последнего использования',
                                           auto_now=True,
                                           blank=True,
                                           null=True)

    class Meta:
        verbose_name = 'Получатель - Категория'
        verbose_name_plural = 'Получатели - Категории'

    def get_url(self):
        return reverse('cat-recipient-detail', args=[self.id])

    def __str__(self):
        return (f'\nНаименование контрагента = {self.recipient.name_recipient},\n'
                f'Наименование категории = {self.category.name_cat},\n'
                f'Время добавления = {self.datetime_add},\n'
                f'Время изменения: {self.datetime_update}\n'
                )
