from django.shortcuts import render, get_object_or_404

from Bot.models import TelegramUser


def show_all_telegram_users(request):
    users = TelegramUser.objects.all()
    return render(request, 'bot/info_users.html', {
        'users': users
    })

def show_telegram_users(request, id_user: int):
    user = get_object_or_404(TelegramUser, id=id_user)
    return render(request, 'bot/one_user.html', {
        'user': user
    })