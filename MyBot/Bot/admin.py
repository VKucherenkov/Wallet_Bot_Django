from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet

from Bot.forms import RegisterUserForm
from Bot.models import TelegramUser, CardUser, CategoryOperation, TypeOperation, OperationUser, Recipient, BankCard, \
    Cat_Recipient, MyUser

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class MyUserAdmin(UserAdmin):
    add_form = RegisterUserForm
    # form = CustomUserChangeForm
    model = MyUser
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'gender', 'birth_date',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(MyUser, MyUserAdmin)

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


@admin.register(BankCard)
class BankCardAdmin(admin.ModelAdmin):
    list_display = ['name_bank',
                    'datetime_add']
    ordering = ['name_bank']
    list_per_page = 10
    search_fields = ['name_bank']


@admin.register(CategoryOperation)
class CategoryOperationAdmin(admin.ModelAdmin):
    list_display = ['name_cat',
                    'TypeOperation_CategoryOperation',
                    'datetime_add',
                    'datetime_update']
    ordering = ['name_cat']
    list_per_page = 10
    search_fields = ['name_cat']


@admin.register(TypeOperation)
class TypeOperationAdmin(admin.ModelAdmin):
    list_display = ['name_type',
                    'datetime_add',
                    'datetime_update']
    ordering = ['name_type']
    list_per_page = 10
    search_fields = ['name_type']


@admin.register(CardUser)
class CardUserAdmin(admin.ModelAdmin):
    list_display = ['name_card',
                    'number_card',
                    'balans_card',
                    'TelegramUser_CardUser',
                    'BankCard_CardUser',
                    'datetime_add',
                    'datetime_update']
    ordering = ['name_card',
                'number_card',
                'balans_card']
    list_per_page = 10
    search_fields = ['name_card',
                     'number_card',
                     'balans_card']


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ['name_recipient',
                    'recipient_in_notification',
                    'datetime_add',
                    'datetime_update']
    ordering = ['name_recipient',
                'recipient_in_notification']
    list_per_page = 10
    search_fields = ['name_recipient',
                     'recipient_in_notification']


@admin.register(OperationUser)
class OperationUserAdmin(admin.ModelAdmin):
    list_display = ['datetime_amount',
                    'amount_operation',
                    'note_operation',
                    'balans',
                    'CardUser_OperationUser',
                    'CategoryOperation_OperationUser',
                    'datetime_add',
                    'datetime_update']
    ordering = ['-datetime_amount',
                'amount_operation',
                'note_operation']
    list_per_page = 10
    search_fields = ['datetime_amount',
                     'amount_operation',
                     'balans',
                     'note_operation']


@admin.register(Cat_Recipient)
class Cat_RecipientAdmin(admin.ModelAdmin):
    list_display = ['category',
                    'recipient',
                    'datetime_add',
                    'datetime_update']
    ordering = ['category',
                'recipient']
    list_per_page = 10
    search_fields = ['category',
                    'recipient']
