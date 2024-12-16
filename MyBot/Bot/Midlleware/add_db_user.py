import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from Bot.Work_db.user_db_create_update import db_telegramuser

logger = logging.getLogger(__name__)

class UserUpdateMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data:Dict[str, Any]) -> Any:
        logger.info('Действие до обработчика')
        await db_telegramuser(event)
        logger.info('Действие до обработчика завершено')
        result = await handler(event, data)
        logger.info('Действия после обработчика')
        return result
