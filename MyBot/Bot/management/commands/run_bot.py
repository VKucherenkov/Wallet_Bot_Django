import asyncio
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from aiogram import Bot, Dispatcher, types

from Bot.Cards.cards import card_work_router
from Bot.FSM_processing.parser_auto import user_parser_router
from Bot.common.cmd_list import cmd
from Bot.main_bot import user_start_router
from Bot.FSM_processing import router as parser_router

logger = logging.getLogger(__name__)

bot = Bot(token=settings.TOKEN_BOT)
dp = Dispatcher()

dp.include_router(parser_router)
dp.include_router(card_work_router)
dp.include_router(user_parser_router)
dp.include_router(user_start_router)


class Command(BaseCommand):
    help = "Запускаем бота"

    def handle(self, *args, **options):
        print('run')
        # try:
        #     asyncio.run(dp.start_polling(bot))
        # except Exception as err:
        #     logger.error(f'Ошибка: {err}')
        async def main():
            await bot.delete_webhook(drop_pending_updates=True)
            # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
            await bot.set_my_commands(commands=cmd, scope=types.BotCommandScopeAllPrivateChats())
            await dp.start_polling(bot)

        asyncio.run(main())

