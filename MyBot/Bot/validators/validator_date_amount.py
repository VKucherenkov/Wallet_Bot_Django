import logging

from aiogram import types

from datetime import datetime
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)

def validator_date_amount(message: types.Message) -> bool:
    """
    Извлекает дату и время из строки сообщения и возвращает булевое значение.

    :param msg: Строка сообщения.
    :return: Объект datetime с временной зоной.
    :raises ValueError: Если формат строки не соответствует ожидаемому.
    """
    try:
        # Извлекаем дату и время из строки
        day, month, year, hours, minutes = map(int, message.text.split(','))

        # Создаем объект datetime
        specific_time = datetime(year, month, day, hours, minutes, 0, 0)

        # Привязываем к временной зоне
        timezone = ZoneInfo('Asia/Novosibirsk')
        specific_time_with_tz = specific_time.replace(tzinfo=timezone)

        logger.info(f"Успешно извлечена дата и время: {specific_time_with_tz}")
        return True

    except (ValueError, IndexError) as err:
        # Логируем ошибку
        logger.error(f"Ошибка при извлечении даты и времени из строки: {message.text}. Ошибка: {err}", exc_info=True)
        raise ValueError(f"Некорректный формат строки: {message.text}") from err

    return False
