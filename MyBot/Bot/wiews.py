import logging

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView

from Bot.forms import RegisterUserForm, LoginUserForm
from Bot.models import TelegramUser, CardUser, TypeOperation, CategoryOperation, OperationUser
from Bot.utils import DataMixin, menu

logger = logging.getLogger(__name__)

class IndexShow(DataMixin, TemplateView):
    template_name = 'bot/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


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


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'bot/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Регистрация')
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'bot/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


def logout_user(request):
    logout(request)
    return redirect('login')


class TelegramUsersShow(DataMixin, ListView):
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
        context['title_col'] = self.title_col
        c_def = self.get_user_context(title='Пользователи бота')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        if self.request.user.username == str(settings.TELEGRAM_ID_ADMIN):
            return TelegramUser.objects.order_by('telegram_id')
        else:
            return TelegramUser.objects.filter(telegram_id=int(self.request.user.username))


class TelegramUserShow(DataMixin, ListView):
    template_name = 'bot/one_user.html'
    context_object_name = 'userdetail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        c_def = self.get_user_context(title='Пользователь бота')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.kwargs['userdetail_slug']
        self.user = TelegramUser.objects.get(slug=slug)
        return TelegramUser.objects.all()


class Cards(DataMixin, ListView):
    template_name = 'bot/cards.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.user
        c_def = self.get_user_context(title='Карты пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug_user = self.kwargs['userdetail_slug']
        self.user = TelegramUser.objects.get(slug=slug_user)
        return CardUser.objects.filter(
            TelegramUser_CardUser=self.user).order_by(
            'number_card').select_related('BankCard_CardUser')


class Types(DataMixin, ListView):
    template_name = 'bot/types.html'
    context_object_name = 'types'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['user'] = TelegramUser.objects.get(slug=slug)
        c_def = self.get_user_context(title='Тип операций')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return TypeOperation.objects.order_by('name_type')


class Categoryes(DataMixin, ListView):
    template_name = 'bot/categoryes.html'
    context_object_name = 'categoryes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['user'] = TelegramUser.objects.get(slug=slug)
        c_def = self.get_user_context(title='Категории операций')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return CategoryOperation.objects.order_by('name_cat')


class AllOperation(DataMixin, ListView):
    template_name = 'bot/all_operation.html'
    context_object_name = 'all_operation'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.kwargs['user']
        c_def = self.get_user_context(title='Все операции')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.kwargs['userdetail_slug']
        self.kwargs['user'] = TelegramUser.objects.get(slug=slug)
        cards_user_id = [i.id for i in CardUser.objects.filter(TelegramUser_CardUser=self.kwargs['user'])]
        return OperationUser.objects.filter(CardUser_OperationUser__in=cards_user_id).order_by('-datetime_add')


def profile_view(request):
    return render(request, 'bot/profile.html')
