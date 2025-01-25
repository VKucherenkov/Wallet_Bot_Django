import logging
from django.core.cache import cache
from django.db import transaction

from asgiref.sync import sync_to_async

from Bot.common.global_variable import banks, data_parser
from Bot.models import BankCard, CardUser

logger = logging.getLogger(__name__)


@sync_to_async
def db_bank_create(cache_timeout: int = 60 * 60):
    """
    Создает записи в таблице BankCard, если они еще не существуют.
    Использует кэширование для оптимизации.
    """
    cache_key = "bank_names_cache"
    bank_names = cache.get(cache_key)

    if bank_names is None:
        # Если данные не в кэше, получаем их из базы данных
        bank_names = list(BankCard.objects.values_list('name_bank', flat=True))
        cache.set(cache_key, bank_names, timeout=cache_timeout)  # Кэшируем на 1 час

    if not bank_names:
        # Если таблица пуста, создаем записи
        banks_to_create = [BankCard(name_bank=name.lower()) for name in banks.keys()]

        # Используем транзакцию для атомарности
        with transaction.atomic():
            BankCard.objects.bulk_create(banks_to_create)

        # Обновляем кэш
        cache.set(cache_key, [b.name_bank for b in banks_to_create], timeout=cache_timeout)

        logger.info(f"Созданы записи для банков: {list(banks.keys())}")
    else:
        logger.info(f'Таблица "Банки" уже была создана. Количество записей: {len(bank_names)}')


@sync_to_async
def get_bank_name_by_card(number_card: int, cache_timeout: int = 60 * 60) -> str | None:
    """
    Возвращает название банка по номеру карты с использованием кэширования.

    :param number_card: Номер карты.
    :param cache_timeout: Время жизни кэша в секундах (по умолчанию 60 минут).
    :return: Название банка или None, если карта не найдена или произошла ошибка.
    """
    cache_key = f"bank_name_{number_card}"  # Уникальный ключ для кэша
    bank_name = cache.get(cache_key)  # Пытаемся получить данные из кэша

    if bank_name is None:  # Если данных нет в кэше
        try:
            # Ищем банк по номеру карты
            bank_name = CardUser.objects.get(number_card=number_card).bank.name_bank
            logger.info(f"Для карты {number_card} найден банк: {bank_name}")
            # Кэшируем результат
            cache.set(cache_key, bank_name, timeout=cache_timeout)
        except BankCard.DoesNotExist:
            logger.error(f"Карта с номером {number_card} не найдена в базе данных.")
            return None
        except Exception as err:
            logger.error(f"Произошла ошибка при поиске банка для карты {number_card}: {err}", exc_info=True)
            return None
    if not bank_name:
        # Ищем банк по номеру карты
        bank_name = CardUser.objects.get(number_card=number_card).bank.name_bank
        # Обновляем кэш
        cache.set(cache_key, bank_name, timeout=cache_timeout)

    return bank_name