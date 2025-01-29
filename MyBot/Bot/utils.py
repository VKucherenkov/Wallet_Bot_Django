from django.conf import settings

menu = [
    {'title': 'О сайте', 'url_link': 'about'},
    {'title': "Обратная связь", 'url_link': 'contact'}
]


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if self.request.user.username == str(settings.TELEGRAM_ID_ADMIN):
            user_menu.append({'title': "Информация о пользователях", 'url_link': 'users'})
        elif self.request.user.is_authenticated:
            user_menu.append({'title': "Информация о пользователе", 'url_link': 'users'})
        context['menu'] = user_menu
        return context
