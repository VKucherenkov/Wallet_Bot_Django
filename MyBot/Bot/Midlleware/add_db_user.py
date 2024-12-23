import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from Bot.Work_db.bank_db import db_bank_create
from Bot.Work_db.category_operation_db import db_categoryoperation_create
from Bot.Work_db.type_operation_db import db_typeoperation_crate
from Bot.Work_db.user_db_create_update import db_telegramuser

logger = logging.getLogger(__name__)


class UserUpdateMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        logger.info('Действие до обработчика')
        await db_telegramuser(event)
        await db_bank_create()
        await db_typeoperation_crate()
        await db_categoryoperation_create()
        logger.info('Действие до обработчика завершено')
        result = await handler(event, data)
        logger.info('Действия после обработчика')
        msg = event.text
        if event.text and '[' in event.text:
            msg_date = msg[msg.index('[') + 1: msg.index('[') + 1 + 10] + ' ' + msg[
                                                                                msg.index(']') + 1 - 6: msg.index(']')]
            logger.info(msg_date)
            logger.info(f'Пользователь написал:\n{event.text}')
        logger.info('Действия после обработчика завершены')

        return result
