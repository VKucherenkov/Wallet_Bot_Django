import logging
from django.core.cache import cache

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from Bot.models import CardUser

logger = logging.getLogger(__name__)


def _format_cards_text(cards: list[dict]) -> str:
    """
    Форматирует список карт в текстовое представление.

    :param cards: Список карт в виде словарей.
    :return: Отформатированный текст.
    """
    if not cards:
        return ""

    # Создаем заголовок таблицы
    headers = cards[0].keys()
    result_txt = ''.join(f'<code>{header:^8}</code>' for header in headers)

    # Добавляем разделитель
    result_txt += '\n' + '-' * 71 + '\n'

    # Добавляем данные
    for card in cards:
        result_txt += ''.join(f'<code>{str(value).upper():^8}</code>' for value in card.values()) + '\n'

    return result_txt

@sync_to_async
def card_list(msg, cache_timeout: int = 60 * 15) -> tuple[str, list[dict]]:
    """
    Возвращает список карт пользователя, отформатированный в виде текста и списка словарей.

    :param cache_timeout: Время хранения кэша (по умолчанию 15 минут)
    :param msg: Объект сообщения.
    :return: Кортеж (отформатированный текст, список карт).
    """
    cache_key = f"user_cards_{msg.from_user.id}"
    cached_result = cache.get(cache_key)

    if cached_result is None:
        try:
            # Фильтруем карты по telegram_id пользователя
            cards = CardUser.objects.filter(telegram_user__telegram_id=msg.from_user.id)
            result_lst = [
                {
                    'ID': card.pk,
                    'Имя': card.name_card,
                    'Номер': card.number_card,
                    'Баланс': card.balans_card,
                }
                for card in cards
            ]

            # Форматируем текст
            result_txt = _format_cards_text(result_lst)

            # Кэшируем результат
            cache.set(cache_key, (result_txt, result_lst), timeout=cache_timeout)  # Кэшируем на 15 минут
            logger.info(f"Загружены карты для пользователя {msg.from_user.id}: {len(result_lst)} шт.")
        except Exception as err:
            logger.error(f"Произошла ошибка при загрузке карт: {err}", exc_info=True)
            return "", []
    else:
        result_txt, result_lst = cached_result

    return result_txt, result_lst


@sync_to_async
def card_number(number_card) -> bool:
    """
    Проверяет, существует ли карта с указанным номером в базе данных.

    :param number_card: Номер карты (строка или число).
    :return: True, если карта существует и номер совпадает, иначе False.
    """
    try:
        # Преобразуем number_card в строку для сравнения
        number_card = str(number_card)
        # Получаем номер карты из базы данных
        number_card_db = CardUser.objects.get(number_card=number_card).number_card
        # Сравниваем номера карт
        return number_card == str(number_card_db)
    except ObjectDoesNotExist:
        logger.info(f"Карта с номером {number_card} не найдена.")
        return False
    except Exception as e:
        logger.error(f"Ошибка при проверке номера карты: {e}")
        return False


@sync_to_async
def card_name(number_card) -> str:
    """
    Возвращает название карты по её номеру.

    :param number_card: Номер карты (строка или число).
    :return: Название карты, если карта найдена, иначе None.
    """
    try:
        # Преобразуем number_card в строку для сравнения
        number_card = str(number_card)
        # Получаем название карты из базы данных
        card_name = CardUser.objects.get(number_card=number_card).name_card
        return card_name
    except ObjectDoesNotExist:
        logger.info(f"Карта с номером {number_card} не найдена.")
        return None
    except Exception as e:
        logger.error(f"Ошибка при получении названия карты: {e}")
        return None


@sync_to_async
def card_list_for_kb(message):
    """
    Возвращает список карт, принадлежащих пользователю, для отображения в клавиатуре.

    :param message: Объект сообщения от пользователя.
    :return: Список словарей с информацией о картах.
    """
    try:
        # Фильтруем карты по telegram_id пользователя
        cards = CardUser.objects.filter(telegram_user__telegram_id=message.from_user.id)

        # Формируем список карт
        result_lst = [
            {
                'ID': card.pk,
                'Имя': card.name_card,
                'Номер': card.number_card,
                'Баланс': card.balans_card,
            }
            for card in cards
        ]

        return result_lst
    except Exception as e:
        logger.error(f"Ошибка при получении списка карт: {e}")
        return []


@sync_to_async
def get_currency_card(number_card):
    currency_card = CardUser.objects.get(number_card=number_card).currency_card
    return currency_card if currency_card else None

@sync_to_async
def get_type_card(number_card):
    type_card = CardUser.objects.get(number_card=number_card).type_card
    return type_card if type_card else None


@sync_to_async
def get_credit_limit_card(number_card):
    credit_limit = CardUser.objects.get(number_card=number_card).credit_limit
    return credit_limit if credit_limit else None