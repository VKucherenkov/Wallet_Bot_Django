from django.shortcuts import render, get_object_or_404

from Bot.models import TelegramUser, CardUser, TypeOperation, CategoryOperation

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


def show_all_telegram_users(request):
    users = TelegramUser.objects.all()
    title_col = [{'title': 'ID пользователя:'},
                 {'title': 'Телеграмм ID:'},
                 {'title': 'Имя пользователя:'},
                 {'title': 'Email:',},
                 {'title': 'Пол:',},
                 {'title': 'Дата регистрации'},
                 {'title': 'Дата последней активности'}]
    context = {
        'menu': menu,
        'users': users,
        'title_col': title_col,
        'title': 'Пользователи бота',
    }
    return render(request, 'bot/info_users.html', context=context)


def show_telegram_users(request, userdetail_slug):
    user = get_object_or_404(TelegramUser, slug=userdetail_slug)
    context = {
        'menu': menu,
        'user': user,
        'title': 'Пользователь бота',
    }
    return render(request, 'bot/one_user.html', context=context)


def get_cards(request, userdetail_slug):
    user = TelegramUser.objects.get(slug=userdetail_slug)
    cards = CardUser.objects.filter(TelegramUser_CardUser=user.id)
    context = {
        'menu': menu,
        'title': 'Карты пользователя',
        'user': user,
        'cards': cards
    }
    return render(request, 'bot/cards.html', context=context)

def get_types(request, userdetail_slug):
    types = TypeOperation.objects.all()
    user = TelegramUser.objects.get(slug=userdetail_slug)
    context = {
        'menu': menu,
        'title': 'Типы операций',
        'user': user,
        'types': types
    }
    return render(request, 'bot/types.html', context=context)

def get_categoryes(request, userdetail_slug):
    categoryes = CategoryOperation.objects.all()
    user = TelegramUser.objects.get(slug=userdetail_slug)
    context = {
        'menu': menu,
        'title': 'Типы операций',
        'user': user,
        'categoryes': categoryes
    }
    return render(request, 'bot/categoryes.html', context=context)