from django.contrib import admin


from Bot.models import TelegramUser, CardUser

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(CardUser)
