import logging

from aiogram import types
from django.core.cache import cache
from django.db import transaction
from asgiref.sync import sync_to_async

from Bot.common.global_variable import data_parser
from Bot.models import TypeOperation, Recipient, CategoryOperation

logger = logging.getLogger(__name__)


@sync_to_async
def db_typeoperation_create(cache_timeout: int = 60 * 60):
    """
    Создает записи в таблице TypeOperation, если они еще не существуют.
    Использует кэширование для оптимизации.
    """
    cache_key = "type_operations_cache"
    type_operations = cache.get(cache_key)

    if type_operations is None:
        # Если данные не в кэше, получаем их из базы данных
        type_operations = list(TypeOperation.objects.values_list('name_type', flat=True))
        cache.set(cache_key, type_operations, timeout=cache_timeout)  # Кэшируем на 1 час

    if not type_operations:
        # Если таблица пуста, создаем записи
        types = ['Доход', 'Расход', 'Перевод между своими счетами', 'возврат']

        # Формируем список объектов для массового создания
        types_to_create = [TypeOperation(name_type=type_name.lower()) for type_name in types]

        # Используем транзакцию для атомарности
        with transaction.atomic():
            for type in types_to_create:
                TypeOperation.objects.update_or_create(name_type=type)

        # Обновляем кэш
        cache.set(cache_key, [t.name_type for t in types_to_create], timeout=cache_timeout)

        logger.info(f"Созданы записи для типов операций: {types}")
    else:
        logger.info(f'Таблица "Тип операции" уже была создана. Количество записей: {len(type_operations)}')


def _get_type_by_keywords(text: str) -> str | None:
    """
    Определяет тип операции на основе ключевых слов в тексте.

    :param text: Текст сообщения.
    :return: Название типа операции или None, если ключевые слова не найдены.
    """
    text_lower = text.lower()

    if any(word in text_lower for word in ['оплата', 'покупка', 'списан']):
        return 'расход'
    elif 'с карты' in text_lower:
        return 'перевод между своими счетами'
    elif any(word in text_lower for word in ['зачисл', 'аванс']):
        return 'доход'
    elif 'возвр' in text_lower:
        return 'возврат'
    return None

@sync_to_async
def name_type(message: types.Message, cache_timeout: int = 60 * 15) -> str | None:
    """
    Определяет тип операции на основе текста сообщения или данных из базы данных.

    :param cache_timeout: Время жизни кэша в секундах (по умолчанию 15 минут).
    :param message: Объект сообщения.
    :return: Название типа операции или None, если тип не удалось определить.
    """
    # Пытаемся определить тип операции по ключевым словам
    type_by_keywords = _get_type_by_keywords(message.text)
    if type_by_keywords:
        logger.info(f"Тип операции определен по ключевым словам: {type_by_keywords}")
        return type_by_keywords

    # Если тип не определен по ключевым словам, обращаемся к базе данных
    cache_key = f"recipient_type_{message.text.lower()}"
    type_name = cache.get(cache_key)

    if type_name is None:
        try:
            recipient = Recipient.objects.get(name_recipient=data_parser['name_recipient'])
            category = CategoryOperation.objects.get(pk=recipient.recipient_id)
            type_name = TypeOperation.objects.get(pk=category.type_id).name_type
            logger.info(f"Тип операции определен из базы данных: {type_name}")
            cache.set(cache_key, type_name, timeout=cache_timeout)  # Кэшируем на 15 минут
        except Recipient.DoesNotExist:
            logger.error(f"Получатель с именем {data_parser['name_recipient']} не найден.")
            return None
        except CategoryOperation.DoesNotExist:
            logger.error(f"Категория операции для получателя {data_parser['name_recipient']} не найдена.")
            return None
        except TypeOperation.DoesNotExist:
            logger.error(f"Тип операции для категории не найден.")
            return None
        except Exception as err:
            logger.error(f"Произошла ошибка при определении типа операции: {err}", exc_info=True)
            return None

    return type_name


@sync_to_async
def get_type_for_keyboard(cache_timeout: int = 60 * 60) -> list[str]:
    """
    Возвращает список названий всех типов операций из таблицы TypeOperation.

    :param cache_timeout: Время жизни кэша в секундах (по умолчанию 60 минут).
    :return: Список названий типов операций.
    """
    cache_key = "all_types_for_keyboard"  # Уникальный ключ для кэша
    types_name = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if types_name is None:  # Если данных нет в кэше
        try:
            # Используем values_list для оптимизации запроса
            types_name = list(TypeOperation.objects.values_list('name_type', flat=True))
            logger.info(f"Загружены типы операций для клавиатуры: {len(types_name)} шт.")
            cache.set(cache_key, types_name, timeout=cache_timeout)  # Кэшируем на 1 час
        except Exception as err:
            logger.error(f"Произошла ошибка при загрузке типов операций: {err}", exc_info=True)
            return []

    return types_name