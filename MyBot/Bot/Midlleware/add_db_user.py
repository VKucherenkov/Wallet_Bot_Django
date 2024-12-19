import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from Bot.Work_db.category_operation_db_create import db_categoryoperation
from Bot.Work_db.type_operation_db_create import db_typeoperation
from Bot.Work_db.user_db_create_update import db_telegramuser

logger = logging.getLogger(__name__)


class UserUpdateMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.info('Действие до обработчика')
        await db_telegramuser(event)
        await db_typeoperation()
        await db_categoryoperation()
        logger.info('Действие до обработчика завершено')
        result = await handler(event, data)
        logger.info('Действия после обработчика')
        msg = event.text
        msg_date = None
        if '[' in event.text:
            msg_date = msg[msg.index('[') + 1: msg.index('[') + 1 + 10] + ' ' + msg[
                                                                                msg.index(']') + 1 - 6: msg.index(']')]
            logger.info(msg_date)
        logger.info(f'Пользователь написал:\n{event.text}')
        logger.info('Действия после обработчика завершены')

        return result
