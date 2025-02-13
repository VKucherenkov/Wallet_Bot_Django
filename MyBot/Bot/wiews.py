import logging
from datetime import datetime
from unicodedata import category

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.db.models import Sum, ExpressionWrapper, F, FloatField, IntegerField
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView, DetailView, UpdateView

from Bot.forms import RegisterUserForm, LoginUserForm, ProfileUpdateForm, AddOperationForm, AddCardForm, \
    AddCategoryForm, AddRecipientForm, AddTypeForm, AddBankForm
from Bot.models import TelegramUser, CardUser, TypeOperation, CategoryOperation, OperationUser, MyUser, Recipient, \
    BankCard
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
        queryset = CardUser.objects.filter(telegram_user=self.user).order_by('number_card').select_related('bank')
        return queryset


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
        queryset = TypeOperation.objects.order_by('name_type')
        return queryset


class Categoryes(DataMixin, ListView):
    template_name = 'bot/categoryes.html'
    context_object_name = 'categoryes'
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['userdetail_slug']
        context['telegram_user'] = TelegramUser.objects.get(slug=slug)
        # Подсчет количества записей
        queryset = self.get_queryset()
        context['total_category'] = queryset.count()

        c_def = self.get_user_context(title='Категории операций')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        # Получаем все категории
        queryset = CategoryOperation.objects.order_by('name_cat')
        return queryset


class AllOperation(DataMixin, ListView):
    model = OperationUser
    template_name = 'bot/all_operation.html'
    context_object_name = 'all_operation'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['telegram_user'] = self.kwargs['user']
        # Передаем параметры фильтрации в контекст для отображения в шаблоне
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['category'] = self.request.GET.get('category', '')
        context['card'] = self.request.GET.get('card', '')

        # Подсчет количества отфильтрованных записей
        queryset = self.get_queryset()
        context['total_operations'] = queryset.count()  # Общее количество записей

        # Передаем списки для выпадающих списков
        context['card'] = CardUser.objects.filter(telegram_user=self.kwargs['user'])
        context['category'] = CategoryOperation.objects.all()

        c_def = self.get_user_context(title='Все операции')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        slug = self.kwargs['userdetail_slug']
        self.kwargs['user'] = TelegramUser.objects.get(slug=slug)
        cards_user_id = [i.id for i in CardUser.objects.filter(telegram_user=self.kwargs['user'])]
        # Получаем все операции для карт пользователя
        queryset = OperationUser.objects.filter(card__in=cards_user_id).order_by('-datetime_add')
        # Применяем фильтры, если они переданы в запросе
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        category = self.request.GET.get('category')
        card = self.request.GET.get('card')
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            queryset = queryset.filter(datetime_amount__gte=start_date)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            queryset = queryset.filter(datetime_amount__lte=end_date)
        if category:
            queryset = queryset.filter(category=category)
        if card:
            queryset = queryset.filter(card=card)
        return queryset


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


class AddCardView(DataMixin, CreateView):
    model = CardUser
    form_class = AddCardForm
    template_name = 'bot/add_card_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_form'] = AddCardForm()
        c_def = self.get_user_context(title='Добавление карты')
        context['next'] = self.request.GET.get('next', '')
        context.update(c_def)
        return context

    def get_success_url(self):
        # Получаем URL для перенаправления из параметра `next`
        next_url = self.request.GET.get('next')
        # Если параметр `next` существует, перенаправляем туда
        if next_url:
            return next_url
        # Если параметр `next` отсутствует, используем URL по умолчанию
        return reverse_lazy('add-operation-form')

    def form_valid(self, form):
        # Получаем объект TelegramUser по telegram_id
        telegram_user = TelegramUser.objects.get(telegram_id=self.request.user.username)
        # Создаем объект CardUser, но не сохраняем его в базу
        card_user = form.save(commit=False)
        # Устанавливаем telegram_user для объекта CardUser
        card_user.telegram_user = telegram_user
        # Сохраняем объект в базу данных
        card_user.save()
        messages.success(self.request, 'Карта добавлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Карта не добавлена!')
        context = self.get_context_data(form=form)
        # context['card_form'] = AddCardForm(self.request.POST)
        return self.render_to_response(context)


class AddTypeView(DataMixin, CreateView):
    model = TypeOperation
    form_class = AddTypeForm
    template_name = 'bot/add_type_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_form'] = AddTypeForm()
        c_def = self.get_user_context(title='Добавление типа операции')
        context.update(c_def)
        return context

    def get_success_url(self):
        # Получаем URL для перенаправления из параметра `next`
        next_url = self.request.GET.get('next')
        # Если параметр `next` существует, перенаправляем туда
        if next_url:
            return next_url
        # Если параметр `next` отсутствует, используем URL по умолчанию
        return reverse_lazy('add-category-form')

    def form_valid(self, form):
        # Сохраняем объект в базу данных
        form.save()
        messages.success(self.request, 'Тип операции добавлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Тип операции не добавлен!')
        context = self.get_context_data(form=form)
        context['type_form'] = AddTypeForm(self.request.POST)
        return self.render_to_response(context)


class AddBankView(DataMixin, CreateView):
    model = BankCard
    form_class = AddBankForm
    template_name = 'bot/add_bank_form.html'
    success_url = reverse_lazy('add-card-form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_form'] = AddTypeForm()
        c_def = self.get_user_context(title='Добавление банка')
        context.update(c_def)
        return context

    def form_valid(self, form):
        # Сохраняем объект в базу данных
        form.save()
        messages.success(self.request, 'Банк добавлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Банк не добавлен!')
        context = self.get_context_data(form=form)
        context['bank_form'] = AddTypeForm(self.request.POST)
        return self.render_to_response(context)


class AddCategoryView(DataMixin, CreateView):
    model = CategoryOperation
    form_class = AddCategoryForm
    template_name = 'bot/add_category_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['category_form'] = AddCategoryForm()
        c_def = self.get_user_context(title='Добавление категории')
        context.update(c_def)
        return context

    def get_success_url(self):
        # Получаем URL для перенаправления из параметра `next`
        next_url = self.request.GET.get('next')
        # Если параметр `next` существует, перенаправляем туда
        if next_url:
            return next_url
        # Если параметр `next` отсутствует, используем URL по умолчанию
        return reverse_lazy('add-operation-form')

    def form_valid(self, form):
        # Сохраняем объект в базу данных
        form.save()
        messages.success(self.request, 'Категория добавлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Категория не добавлена!')
        context = self.get_context_data(form=form)
        return self.render_to_response(context)


class AddRecipientView(DataMixin, CreateView):
    model = Recipient
    form_class = AddRecipientForm
    template_name = 'bot/add_recipient_form.html'
    success_url = reverse_lazy('add-operation-form')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipient_form'] = AddCategoryForm()
        c_def = self.get_user_context(title='Добавление получателя')
        context.update(c_def)
        return context

    def form_valid(self, form):
        # Сохраняем объект в базу данных
        form.save()
        messages.success(self.request, 'Получатель добавлен!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Получатель не добавлен!')
        context = self.get_context_data(form=form)
        context['recipient_form'] = AddRecipientForm(self.request.POST)
        return self.render_to_response(context)


class AddOperationView(DataMixin, CreateView):
    model = OperationUser
    form_class = AddOperationForm
    template_name = 'bot/add_operation_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Передаем пользователя
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление операции')
        context.update(c_def)
        return context

    def get_success_url(self):
        # Получаем URL для перенаправления из параметра `next`
        next_url = self.request.GET.get('next')
        # Если параметр `next` существует, перенаправляем туда
        if next_url:
            return next_url
        # Если параметр `next` отсутствует, используем URL по умолчанию
        return reverse_lazy('add-operation-form')

    def form_valid(self, form):
        card = form.cleaned_data['card']
        card.balans_card = form.cleaned_data.get('balans')
        card.save()
        form.save()
        messages.success(self.request, 'Операция добавлена!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.success(self.request, 'Операция не добавлена!')
        context = self.get_context_data(form=form)
        context['operation_form'] = AddOperationForm(self.request.POST, user=self.request.user)
        return self.render_to_response(context)


class FinanceReport(DataMixin, ListView):
    model = OperationUser
    template_name = 'bot/finance_report.html'
    context_object_name = 'finance_report'

    def get_queryset(self):
        """
        Возвращает отфильтрованный QuerySet для операций пользователя.
        """
        # Получаем пользователя и его карты
        slug = self.kwargs['userdetail_slug']
        self.kwargs['user'] = TelegramUser.objects.get(slug=slug)
        self.cards = CardUser.objects.filter(telegram_user=self.kwargs['user'])

        # Применяем фильтры, если они переданы в запросе
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        card = self.request.GET.get('card')

        # Фильтруем операции по картам и категориям
        queryset = OperationUser.objects.filter(
            card__in=self.cards,
            category__type__name_type__in=['расход', 'Тип операции: расход']
        ).values('category__name_cat').annotate(
            total_amount=Sum('amount_operation')
        ).order_by('category__name_cat')

        # Применяем фильтры по датам и карте
        queryset = self.apply_filters(queryset, start_date, end_date, card)

        # Вычисляем общую сумму и процент для каждой категории
        self.total_sum = queryset.aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0
        queryset = queryset.annotate(
            percentage=ExpressionWrapper(
                F('total_amount') * 100.0 / self.total_sum,
                output_field=FloatField()
            )
        )
        return queryset

    def get_context_data(self, **kwargs):
        """
        Добавляет дополнительные данные в контекст шаблона.
        """
        context = super().get_context_data(**kwargs)

        # Передаем пользователя и параметры фильтрации в контекст
        context['telegram_user'] = self.kwargs['user']
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['card'] = self.request.GET.get('card', '')
        context['cards'] = self.cards

        # Подсчет общей суммы и количества записей для расходов
        queryset = self.object_list
        context['total_count'] = queryset.count()
        # total_sum = queryset.aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0
        context['total_sum'] = self.total_sum

        # Фильтрация и агрегация данных для доходов
        queryset_expense = self.get_expense_queryset()
        context['queryset_expense'] = queryset_expense
        context['total_sum_expense'] = self.total_sum_expense
        context['total_difference'] = context['total_sum_expense'] - context['total_sum']
        context['total_percentage_expense'] = self.get_total_percentage(queryset_expense) # Вызов функции для получения общего процента
        context['total_percentage_income'] = self.get_total_percentage(queryset) # Вызов функции для получения общего процента


        # Добавляем пользовательский контекст из миксина
        c_def = self.get_user_context(title='Все операции')
        return {**context, **c_def}

    def get_expense_queryset(self):
        """
        Возвращает QuerySet для операций доходов с фильтрацией и агрегацией.
        """
        queryset = OperationUser.objects.filter(
            card__in=self.cards,
            category__type__name_type__in=['Тип операции: доход']
        ).values('category__name_cat').annotate(
            total_amount=Sum('amount_operation')
        ).order_by('category__name_cat')

        # Применяем фильтры по датам
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        queryset = self.apply_filters(queryset, start_date, end_date)

        # Вычисляем общую сумму и процент для каждой категории
        self.total_sum_expense = queryset.aggregate(total_sum=Sum('total_amount'))['total_sum'] or 0
        queryset = queryset.annotate(
            percentage=ExpressionWrapper(
                F('total_amount') * 100.0 / self.total_sum_expense,
                output_field=FloatField()
            )
        )
        return queryset

    def get_total_percentage(self, queryset):
        total_percentage = queryset.aggregate(total_percentage=Sum('percentage'))
        return total_percentage.get('total_percentage')

    def apply_filters(self, queryset, start_date=None, end_date=None, card=None):
        """
        Применяет фильтры по датам и карте к переданному QuerySet.
        """
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                queryset = queryset.filter(datetime_amount__gte=start_date)
            except ValueError:
                pass  # Игнорируем некорректные даты

        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(datetime_amount__lte=end_date)
            except ValueError:
                pass  # Игнорируем некорректные даты

        if card:
            queryset = queryset.filter(card=card)

        return queryset
