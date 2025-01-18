
menu = [{'title': 'О сайте', 'url_link': 'about'},
        {'title': "Информация о пользователях", 'url_link': 'users'},
        # {'title': "Информация о пользователе", 'url_link': 'userdetail'},
        {'title': "Обратная связь", 'url_link': 'contact'},
        ]

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context