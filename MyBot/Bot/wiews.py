import logging

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView

from Bot.models import TelegramUser, CardUser, TypeOperation, CategoryOperation, OperationUser

logger = logging.getLogger(__name__)

menu = [{'title': 'О сайте', 'url_link': 'about'},
        {'title': "Информация о пользователях", 'url_link': 'users'},
        {'title': "Обратная связь", 'url_link': 'contact'},
        {'title': "Войти", 'url_link': 'login_in'}]


def index(request):
    context = {
        'menu': menu,
        'title': 'Главная страница',
    }
    return render(request, 'bot/index.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте',
        'description': 'Описание работы сайта'
    }
    return render(request, 'bot/about.html', context=context)


def contact(request):
    context = {
        'menu': menu,
        'title': 'Контакты',
        'description': 'Наши контакты для связи'
    }
    return render(request, 'bot/about.html', context=context)


def login_in(request):
    context = {
        'menu': menu,
        'title': 'Вход',
        'description': 'Введите данные для входа в аккаунт'
    }
    return render(request, 'bot/about.html', context=context)


class TelegramUsersShow(ListView):
    template_name = 'bot/info_users.html'
    context_object_name = 'users'
    title_col = [{'title': 'ID пользователя:'},
                 {'title': 'Телеграмм ID:'},
                 {'title': 'Имя пользователя:'},
                 {'title': 'Email:', },
                 {'title': 'Пол:', },
                 {'title': 'Дата регистрации'},
                 {'title': 'Дата последней активности'}]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи бота'
        context['menu'] = menu
        context['title_col'] = self.title_col
        return context

    def get_queryset(self):
        return TelegramUser.objects.order_by('telegram_id')


class TelegramUserShow(ListView):
    template_name = 'bot/one_user.html'
    context_object_name = 'userdetail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['title'] = 'Пользователь бота'
        context['menu'] = menu
        context['user'] = TelegramUser.objects.get(slug=slug)
        return context

    def get_queryset(self):
        return TelegramUser.objects.all()


class Cards(ListView):
    template_name = 'bot/cards.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug_user = self.kwargs['userdetail_slug']
        context['title'] = 'Карты пользователя'
        context['menu'] = menu
        context['user'] = TelegramUser.objects.get(slug=slug_user)
        return context

    def get_queryset(self):
        slug_user = self.kwargs['userdetail_slug']
        return CardUser.objects.filter(
            TelegramUser_CardUser=TelegramUser.objects.get(slug=slug_user).id).order_by(
            'number_card')


class Types(ListView):
    template_name = 'bot/types.html'
    context_object_name = 'types'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['title'] = 'Тип операций'
        context['menu'] = menu
        context['user'] = TelegramUser.objects.get(slug=slug)
        return context

    def get_queryset(self):
        return TypeOperation.objects.order_by('name_type')


class Categoryes(ListView):
    template_name = 'bot/categoryes.html'
    context_object_name = 'categoryes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['title'] = 'Категории операций'
        context['menu'] = menu
        context['user'] = TelegramUser.objects.get(slug=slug)
        return context

    def get_queryset(self):
        return CategoryOperation.objects.order_by('name_cat')


class AllOperation(ListView):
    template_name = 'bot/all_operation.html'
    context_object_name = 'all_operation'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['title'] = 'Все операции'
        context['menu'] = menu
        context['user'] = TelegramUser.objects.get(slug=slug)
        return context

    def get_queryset(self):
        slug = self.kwargs['userdetail_slug']
        user_id = TelegramUser.objects.get(slug=slug).id
        cards_user_id = [i.id for i in CardUser.objects.filter(TelegramUser_CardUser=user_id)]
        return OperationUser.objects.filter(CardUser_OperationUser__in=cards_user_id).order_by('-datetime_add')
