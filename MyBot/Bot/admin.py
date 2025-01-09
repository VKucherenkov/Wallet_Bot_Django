from django.contrib import admin
from django.db.models import QuerySet

from Bot.models import TelegramUser, CardUser, CategoryOperation, TypeOperation, OperationUser, Recipient, BankCard, \
    Cat_Recipient

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id', 'email', 'first_name', 'last_name', 'gender', 'datetime_add', 'datetime_update']
    list_editable = ['email', 'first_name', 'last_name', 'gender']
    ordering = ['datetime_update']
    list_per_page = 5
    actions = ['set_male', 'set_female']
    search_fields = ['telegram_id', 'email__startswith', 'first_name']

    @admin.action(description='Установить пол в мужской')
    def set_male(self, request, qs: QuerySet):
        count_update = qs.update(gender=TelegramUser.MALE)
        self.message_user(
            request,
            f'Было обновлено {count_update} записей'
        )

    @admin.action(description='Установить пол в женский')
    def set_female(self, request, qs: QuerySet):
        count_update = qs.update(gender=TelegramUser.FEMALE)
        self.message_user(
            request,
            f'Было обновлено {count_update} записей'
        )

# Register your models here.
admin.site.register(BankCard)
admin.site.register(CardUser)
admin.site.register(CategoryOperation)
admin.site.register(TypeOperation)
admin.site.register(OperationUser)
admin.site.register(Recipient)
admin.site.register(Cat_Recipient)
