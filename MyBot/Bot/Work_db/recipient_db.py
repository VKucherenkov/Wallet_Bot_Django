import logging

from asgiref.sync import sync_to_async

from Bot.models import Recipient


from django.core.cache import cache


logger = logging.getLogger(__name__)

from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

@sync_to_async
def get_recipient_db(data: str, cache_timeout: int = 60 * 60) -> list[str] | None:
    """
    Возвращает список имен получателей из таблицы Recipient.

    :param data: Имя получателя для проверки и добавления.
    :param cache_timeout: Время жизни кэша в секундах.
    :return: Список имен получателей или None, если произошла ошибка.
    """
    cache_key = "all_recipients"  # Уникальный ключ для кэша
    recipients_lst = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if recipients_lst is None or data.lower() not in [name.lower() for name in recipients_lst]:  # Если данных нет в кэше
        try:
            # Используем values_list для оптимизации запроса
            recipients = Recipient.objects.values_list('name_recipient', flat=True)
            recipients_lst = [name.capitalize() for name in recipients]
            logger.info(f"Загружены получатели: {len(recipients_lst)} шт.")
            cache.set(cache_key, recipients_lst, timeout=cache_timeout)  # Кэшируем на 1 час
        except Exception as err:
            logger.error(f"Произошла ошибка при загрузке получателей: {err}", exc_info=True)
            return None

    return recipients_lst
