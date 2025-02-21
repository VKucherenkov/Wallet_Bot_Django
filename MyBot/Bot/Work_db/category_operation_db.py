import logging
from django.core.cache import cache
from django.db import transaction
from asgiref.sync import sync_to_async

from Bot.common.global_variable import categoryes, type_category
from Bot.models import CategoryOperation, TypeOperation, Recipient, OperationUser

logger = logging.getLogger(__name__)


@sync_to_async
def db_categoryoperation_create(cache_timeout: int = 60 * 60):
    """
    Создает записи в таблице CategoryOperation, если они еще не существуют.
    Использует кэширование для оптимизации.
    """
    cache_key = "category_operations_cache"
    category_operations = cache.get(cache_key)

    if category_operations is None:
        # Если данные не в кэше, получаем их из базы данных
        category_operations = list(CategoryOperation.objects.values_list('name_cat', flat=True))
        cache.set(cache_key, category_operations, timeout=cache_timeout)  # Кэшируем на 1 час

    if not category_operations:
        # Если таблица пуста, создаем записи
        cat = [i for i in categoryes.keys()]
        typeoperation = [(i, j) for i in cat for j, value in type_category.items() if i in value]

        # Получаем все типы операций за один запрос
        type_operations = {op.name_type.lower(): op.pk for op in TypeOperation.objects.all()}

        # Формируем список объектов для массового создания
        categories_to_create = [
            CategoryOperation(name_cat=i.lower(), type_id=type_operations[j.lower()])
            for i, j in typeoperation
        ]

        # Используем транзакцию для атомарности
        with transaction.atomic():
            for category in  categories_to_create:
                CategoryOperation.objects.update_or_create(name_cat=category.name_cat, type=category.type)

        # Обновляем кэш
        cache.set(cache_key, [c.name_cat for c in categories_to_create], timeout=cache_timeout)

        logger.info(f"Созданы записи для категорий операций: {cat}")
    else:
        logger.info(f'Таблица "Категория операции" уже была создана. Количество записей: {len(category_operations)}')


@sync_to_async
def get_name_category(name_recipient: str, cache_timeout: int = 60) -> str | None:
    """
    Возвращает название категории для получателя по его имени, если она единственная.

    :param cache_timeout: Время хранения кэша (секунд)
    :param name_recipient: Имя получателя.
    :return: Название категории или None, если получатель не найден, категорий нет или их больше одной.
    """
    cache_key = f"recipient_category_{name_recipient.lower()}"  # Уникальный ключ для кэша
    category_name = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if category_name is None:  # Если данных нет в кэше
        try:
            recipient = Recipient.objects.get(name_recipient=name_recipient.lower())
            operation_this_recipient = OperationUser.objects.filter(recipient=recipient)
            categories = set([i.category.name_cat for i in operation_this_recipient])

            if len(categories) == 1:
                category_name = categories.pop()
                logger.info(f"Для получателя {name_recipient} найдена категория: {category_name}")
                cache.set(cache_key, category_name, timeout=cache_timeout)  # Кэшируем на 15 минут
            elif len(categories) > 1:
                logger.warning(f"Для получателя {name_recipient} найдено несколько категорий.")
                return None
            else:
                logger.warning(f"Для получателя {name_recipient} категории не найдены.")
                return None
        except Recipient.DoesNotExist:
            logger.error(f"Получатель с именем {name_recipient} не найден.")
            return None
        except Exception as err:
            logger.error(f"Произошла ошибка при поиске категории для получателя {name_recipient}: {err}", exc_info=True)
            return None

    return category_name


@sync_to_async
def get_name_category_auto(data: str, cache_timeout: int = 60) -> list[str] | None:
    """
    Возвращает список названий категорий для получателя по его имени.

    :param cache_timeout: Время хранения кэша (секунд)
    :param data: Имя получателя.
    :return: Список названий категорий или None, если получатель не найден или произошла ошибка.
    """
    cache_key = f"recipient_categories_{data.lower()}"  # Уникальный ключ для кэша
    categories_name = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if categories_name is None:  # Если данных нет в кэше
        try:
            recipient = Recipient.objects.get(name_recipient=data.lower())
            operation_this_recipient = OperationUser.objects.filter(recipient=recipient)
            categories_name = list(set([i.category.name_cat for i in operation_this_recipient]))
            # categories_name = [category.name_cat for category in categories]
            logger.info(f"Для получателя {data} найдены категории: {categories_name}")
            cache.set(cache_key, categories_name, timeout=cache_timeout)  # Кэшируем на 15 минут
        except Recipient.DoesNotExist:
            logger.error(f"Получатель с именем {data} не найден.")
            return None
        except Exception as err:
            logger.error(f"Произошла ошибка при поиске категорий для получателя {data}: {err}", exc_info=True)
            return None

    return categories_name


@sync_to_async
def get_categories_for_keyboard(cache_timeout: int = 60 * 60) -> list[str]:
    """
    Возвращает список названий всех категорий из таблицы CategoryOperation.

    :return: Список названий категорий.
    """
    cache_key = "all_categories_for_keyboard"  # Уникальный ключ для кэша
    categories_name = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if categories_name is None:  # Если данных нет в кэше
        try:
            # Используем values_list для оптимизации запроса
            categories_name = list(CategoryOperation.objects.values_list('name_cat', flat=True))
            logger.info(f"Загружены категории для клавиатуры: {len(categories_name)} шт.")
            cache.set(cache_key, categories_name, timeout=cache_timeout)  # Кэшируем на 1 час
        except Exception as err:
            logger.error(f"Произошла ошибка при загрузке категорий: {err}", exc_info=True)
            return []

    return categories_name