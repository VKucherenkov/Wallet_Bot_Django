import logging
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView

from Bot.forms import RegisterUserForm, LoginUserForm, ProfileUpdateForm, AddOperationForm, AddCardForm, \
    AddCategoryForm, AddRecipientForm
from Bot.models import TelegramUser, CardUser, TypeOperation, CategoryOperation, OperationUser, MyUser
from Bot.utils import DataMixin

logger = logging.getLogger(__name__)


class IndexShow(DataMixin, TemplateView):
    template_name = 'bot/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_t'] = TelegramUser.objects.get(telegram_id=self.request.user.username)
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


class AnaliticsShow(DataMixin, TemplateView):
    template_name = 'bot/analitics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Аналитика')
        return dict(list(context.items()) + list(c_def.items()))


class SecurityShow(DataMixin, TemplateView):
    template_name = 'bot/security.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Безопасность')
        return dict(list(context.items()) + list(c_def.items()))


class InterfaceShow(DataMixin, TemplateView):
    template_name = 'bot/interface.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_t'] = TelegramUser.objects.get(telegram_id=self.request.user.username)
        c_def = self.get_user_context(title='Интерфейс')
        return dict(list(context.items()) + list(c_def.items()))


class AnalizShow(DataMixin, TemplateView):
    template_name = 'bot/analiz.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_t'] = TelegramUser.objects.get(telegram_id=self.request.user.username)
        c_def = self.get_user_context(title='Анализ')
        return dict(list(context.items()) + list(c_def.items()))


class AddOperationShow(DataMixin, TemplateView):
    template_name = 'bot/add_operation_text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_t'] = TelegramUser.objects.get(telegram_id=self.request.user.username)
        c_def = self.get_user_context(title='Добавление данных')
        return dict(list(context.items()) + list(c_def.items()))


class AboutShow(DataMixin, TemplateView):
    template_name = 'bot/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте', description='Описание работы сайта')
        return dict(list(context.items()) + list(c_def.items()))


class ContactShow(DataMixin, TemplateView):
    template_name = 'bot/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Контакты', description='Наши контакты для связи')
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'bot/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        user_in = TelegramUser.objects.filter(telegram_id=form.instance.username)
        if not user_in:
            user_in = TelegramUser.objects.create(telegram_id=form.instance.username,
                                                  first_name=form.instance.first_name,
                                                  last_name=form.instance.last_name,
                                                  email=form.instance.email,
                                                  gender=form.instance.gender,
                                                  )
        else:
            user_in.update(first_name=form.instance.first_name,
                           last_name=form.instance.last_name,
                           email=form.instance.email,
                           gender=form.instance.gender, )
        login(self.request, user)

        return redirect(f'{user_in.get_url()}')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
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
            return TelegramUser.objects.filter(telegram_id=self.request.user.username)


class TelegramUserShow(DataMixin, DetailView):
    model = TelegramUser
    template_name = 'bot/one_user.html'
    context_object_name = 'telegram_user'
    slug_field = 'slug'  # Поле модели, используемое для поиска
    slug_url_kwarg = 'userdetail_slug'  # Имя параметра в URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = datetime.now()
        c_def = self.get_user_context(title='Пользователь бота')
        return dict(list(context.items()) + list(c_def.items()))


class Cards(DataMixin, ListView):
    template_name = 'bot/cards.html'
    context_object_name = 'cards'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_user'] = self.user
        c_def = self.get_user_context(title='Карты пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug_user = self.kwargs['userdetail_slug']
        self.user = TelegramUser.objects.get(slug=slug_user)
        return CardUser.objects.filter(
            telegram_user=self.user).order_by(
            'number_card').select_related('bank')


class Types(DataMixin, ListView):
    template_name = 'bot/types.html'
    context_object_name = 'types'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['telegram_user'] = TelegramUser.objects.get(slug=slug)
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
        context['telegram_user'] = TelegramUser.objects.get(slug=slug)
        c_def = self.get_user_context(title='Категории операций')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return CategoryOperation.objects.order_by('name_cat')


class AllOperation(DataMixin, ListView):
    template_name = 'bot/all_operation.html'
    context_object_name = 'all_operation'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_user'] = self.kwargs['user']
        c_def = self.get_user_context(title='Все операции')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.kwargs['userdetail_slug']
        self.kwargs['user'] = TelegramUser.objects.get(slug=slug)
        cards_user_id = [i.id for i in CardUser.objects.filter(telegram_user=self.kwargs['user'])]
        return OperationUser.objects.filter(card__in=cards_user_id).order_by('-datetime_add')


class MyUserUpdate(DataMixin, UpdateView):
    model = MyUser
    form_class = ProfileUpdateForm
    template_name = 'bot/profile.html'
    success_url = reverse_lazy('home')
    slug_field = 'slug'  # Поле модели, используемое для поиска
    slug_url_kwarg = 'profile_slug'  # Имя параметра в URL

    def form_valid(self, form):
        form_update = form.cleaned_data
        telegram_id = form_update.pop('username', None)
        TelegramUser.objects.filter(telegram_id=telegram_id).update(**form_update)
        messages.success(self.request, 'Профиль обновлен!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все операции')
        return dict(list(context.items()) + list(c_def.items()))


class AddOperationView(DataMixin, CreateView):
    model = OperationUser
    form_class = AddOperationForm
    template_name = 'bot/add_operation_form.html'
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_form'] = AddCardForm()
        context['category_form'] = AddCategoryForm()
        context['recipient_form'] = AddRecipientForm()
        c_def = self.get_user_context(title='Добавление операции')
        context.update(c_def)
        return context

    def form_valid(self, form):
        operation_form = form
        card_form = AddCardForm(self.request.POST)
        category_form = AddCategoryForm(self.request.POST)
        recipient_form = AddRecipientForm(self.request.POST)

        if (operation_form.is_valid() and card_form.is_valid() and
                category_form.is_valid() and recipient_form.is_valid()):
            card = card_form.save(commit=False)
            card.telegram_user = TelegramUser.objects.get(telegram_id=self.user.username)
            card.save()

            category = category_form.save(commit=False)
            category.save()

            recipient = recipient_form.save(commit=False)
            recipient.save()

            operation = operation_form.save(commit=False)
            operation.card = card
            operation.category = category
            operation.recipient = recipient
            operation.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        context['card_form'] = AddCardForm(self.request.POST)
        context['category_form'] = AddCategoryForm(self.request.POST)
        context['recipient_form'] = AddRecipientForm(self.request.POST)
        return self.render_to_response(context)