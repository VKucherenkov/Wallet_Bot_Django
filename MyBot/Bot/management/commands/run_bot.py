import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from aiogram import Bot, Dispatcher, types

from Bot.Midlleware.add_db_user import UserUpdateMiddleware
from Bot.common.cmd_list import cmd
from Bot.routers import router as main_router

logger = logging.getLogger(__name__)

bot = Bot(token=settings.TOKEN_BOT)
dp = Dispatcher()

dp.include_router(main_router)


main_router.message.outer_middleware(UserUpdateMiddleware())


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        print('run')

        async def main():
            await bot.delete_webhook(drop_pending_updates=True)
            await bot.set_my_commands(commands=cmd, scope=types.BotCommandScopeAllPrivateChats())
            await dp.start_polling(bot)

        asyncio.run(main())

