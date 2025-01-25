import logging
from django.core.cache import cache

from asgiref.sync import sync_to_async

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

# @sync_to_async
# def card_list(msg):
#     cards = CardUser.objects.all()
#     # logger.info(cards)
#     result_dict = {}
#     result_lst = []
#     if cards:
#         for i in cards:
#             if i.telegram_user.telegram_id == msg.from_user.id:
#                 result_dict['ID'] = i.pk
#                 result_dict['Имя'] = i.name_card
#                 result_dict['Номер '] = i.number_card
#                 result_dict['Баланс'] = i.balans_card
#             result_lst += [result_dict.copy()]
#     # logger.info(result_lst)
#     result_txt = ''
#     for i in result_dict.keys():
#         result_txt += f'<code>{i:^8}</code>'
#     if result_lst:
#         result_txt += '\n' + '-' * 71 + '\n'
#     for n, i in enumerate(result_lst, 1):
#         for j in i.values():
#             result_txt += f'<code>{str(j).upper():^8}</code>'
#         result_txt += '\n'
#     # logger.info(result_txt)
#     return result_txt, result_lst


@sync_to_async
def card_number(number_card) -> bool:
    try:
        number_card_db = CardUser.objects.get(number_card=number_card).number_card
    except Exception as err:
        logger.info(err)
        return False
    # logger.info(number_card, number_card_db)
    return int(number_card) == number_card_db


@sync_to_async
def card_name(number_card) -> str:
    try:
        card_name = CardUser.objects.get(number_card=number_card).name_card
    except Exception:
        return
    return card_name


@sync_to_async
def card_balance(number_card) -> str:
    try:
        card_name = CardUser.objects.get(number_card=number_card).name_card
    except Exception:
        return
    return card_name


@sync_to_async
def card_list_for_kb(msg):
    cards = CardUser.objects.all()
    # logger.info(cards)
    result_dict = {}
    result_lst = []
    if cards:
        for i in cards:
            if i.telegram_user.telegram_id == msg.from_user.id:
                result_dict['ID'] = i.pk
                result_dict['Имя'] = i.name_card
                result_dict['Номер'] = i.number_card
                result_dict['Баланс'] = i.balans_card
                result_lst += [result_dict.copy()]
    return result_lst