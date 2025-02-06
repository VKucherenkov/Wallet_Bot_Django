import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from Bot.Work_db.bank_db import db_bank_create
from Bot.Work_db.category_operation_db import db_categoryoperation_create
from Bot.Work_db.type_operation_db import db_typeoperation_create
from Bot.Work_db.user_db_create_update import db_telegramuser

logger = logging.getLogger(__name__)

class UserUpdateMiddleware(BaseMiddleware):
    """
    Middleware для обновления данных пользователя и выполнения дополнительных действий
    до и после обработки сообщения.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        """
        Выполняет действия до и после обработки события.

        :param handler: Обработчик события.
        :param event: Событие (например, сообщение).
        :param data: Данные, связанные с событием.
        :return: Результат выполнения обработчика.
        """
        try:
            # Логируем начало обработки
            logger.info(f"Действие до обработчика. Тип события: {event.__class__.__name__}")

            # Обновляем данные пользователя и создаём записи в базе данных
            await self.update_user_data(event)
            await self.create_initial_data()

            # Логируем завершение предобработки
            logger.info("Действие до обработчика завершено")

            # Вызываем обработчик
            result = await handler(event, data)

            # Логируем начало постобработки
            logger.info("Действия после обработчика")

            # Логируем сообщение, если это текст и содержит '['
            if isinstance(event, Message) and event.text and '[' in event.text:
                await self.log_message_with_date(event.text)

            # Логируем завершение постобработки
            logger.info("Действия после обработчика завершены")

            return result
        except Exception as e:
            logger.error(f"Ошибка в middleware: {e}")
            raise

    async def update_user_data(self, event: TelegramObject) -> None:
        """
        Обновляет данные пользователя в базе данных.

        :param event: Событие (например, сообщение).
        """
        if isinstance(event, Message):
            await db_telegramuser(event)

    async def create_initial_data(self) -> None:
        """
        Создаёт начальные данные в базе данных (банки, типы операций, категории).
        """
        await db_bank_create()
        await db_typeoperation_create()
        await db_categoryoperation_create()

    async def log_message_with_date(self, text: str) -> None:
        """
        Логирует сообщение с датой, если оно содержит '['.

        :param text: Текст сообщения.
        """
        try:
            msg_date = text[text.index('[') + 1: text.index('[') + 11] + ' ' + text[
                                                                                text.index(']') - 5: text.index(']')]
            logger.info(f"Дата из сообщения: {msg_date}")
            logger.info(f"Пользователь написал:\n{text}")
        except ValueError:
            logger.warning("Не удалось извлечь дату из сообщения.")