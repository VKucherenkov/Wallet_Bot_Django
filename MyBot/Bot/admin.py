from django.contrib import admin


from Bot.models import TelegramUser, CardUser, CategoryOperation, TypeOperation, OperationUser

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(CardUser)
admin.site.register(CategoryOperation)
admin.site.register(TypeOperation)
admin.site.register(OperationUser)
