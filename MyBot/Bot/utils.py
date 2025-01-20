from MyBot.settings import TELEGRAM_ID_ADMIN
from django.shortcuts import redirect

from Bot.models import TelegramUser

menu = [{'title': 'О сайте', 'url_link': 'about'},
        {'title': "Обратная связь", 'url_link': 'contact'},
        ]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if self.request.user.is_authenticated and int(self.request.user.username) not in [i.telegram_id for i in
                                                                                          TelegramUser.objects.all()]:
            TelegramUser.objects.create(telegram_id=self.request.user.username,
                                first_name=self.request.user.first_name,
                                last_name=self.request.user.last_name,
                                email=self.request.user.email,
                                )
        elif self.request.user.is_authenticated:
            user = TelegramUser.objects.get(telegram_id=self.request.user.username)
            user.first_name = self.request.user.first_name
            user.last_name = self.request.user.last_name
            user.email = self.request.user.email
            user.save()

            # user.objects.create(
            #             first_name=self.request.user.first_name,
            #             last_name=self.request.user.last_name,
            #             email=self.request.user.email,
            #             )
        if self.request.user.username == str(TELEGRAM_ID_ADMIN):
            user_menu.append({'title': "Информация о пользователях", 'url_link': 'users'})
        elif self.request.user.is_authenticated:
            user_menu.append({'title': "Информация о пользователе", 'url_link': 'users'})
        context['menu'] = user_menu
        return context
