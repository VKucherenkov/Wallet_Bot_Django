from django.contrib import admin


from Bot.models import TelegramUser, CardUser, CategoryOperation, TypeOperation, OperationUser, Recipient, BankCard

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(BankCard)
admin.site.register(CardUser)
admin.site.register(CategoryOperation)
admin.site.register(TypeOperation)
admin.site.register(OperationUser)
admin.site.register(Recipient)
