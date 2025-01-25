import logging
from django.core.cache import cache

from asgiref.sync import sync_to_async
from django.utils import timezone

from Bot.models import TelegramUser

logger = logging.getLogger(__name__)



@sync_to_async
def db_telegramuser(msg, cache_timeout: int = 60 * 60) -> None:
    """
    Добавляет или обновляет данные пользователя Telegram в базе данных.

    :param cache_timeout: Время хранения кэша (по умолчанию 60 минут)
    :param msg: Объект сообщения.
    """
    cache_key = f"telegram_user_{msg.from_user.id}"
    user_exists = cache.get(cache_key)

    if user_exists is None:
        # Проверяем, существует ли пользователь в базе данных
        user_exists = TelegramUser.objects.filter(telegram_id=msg.from_user.id).exists()
        cache.set(cache_key, user_exists, timeout=cache_timeout)  # Кэшируем на 1 час

    if not user_exists:
        # Если пользователь не существует, создаем новую запись
        TelegramUser.objects.update_or_create(
            telegram_id=msg.from_user.id,
            defaults={
                'first_name': msg.chat.first_name,
                'last_name': msg.chat.last_name,
            }
        )
        logger.info(
            f'Пользователь {msg.from_user.id} {msg.chat.first_name} {msg.chat.last_name} добавлен в базу данных'
        )
    else:
        # Если пользователь существует, обновляем его данные
        TelegramUser.objects.filter(telegram_id=msg.from_user.id).update(
            datetime_update=timezone.now()  # Обновляем поле datetime_update
        )
        logger.info(
            f'Данные пользователя {msg.from_user.id} {msg.chat.first_name} {msg.chat.last_name} обновлены в базе данных'
        )