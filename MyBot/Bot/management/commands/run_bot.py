import asyncio
from django.core.management.base import BaseCommand

from Bot.main_bot import bot


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        print('run')
        asyncio.run(bot.infinity_polling())


