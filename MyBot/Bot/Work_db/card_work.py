import logging

from asgiref.sync import sync_to_async

from Bot.models import CardUser

logger = logging.getLogger(__name__)


@sync_to_async
def card_list(msg):
    cards = CardUser.objects.all()
    # logger.info(cards)
    result_dict = {}
    result_lst = []
    if cards:
        for i in cards:
            if i.TelegramUser_CardUser.telegram_id == msg.from_user.id:
                result_dict['ID'] = i.pk
                result_dict['Имя'] = i.name_card
                result_dict['Номер '] = i.number_card
                result_dict['Баланс'] = i.balans_card
            result_lst += [result_dict.copy()]
    # logger.info(result_lst)
    result_txt = ''
    for i in result_dict.keys():
        result_txt += f'<code>{i:^8}</code>'
    if result_lst:
        result_txt += '\n' + '-' * 71 + '\n'
    for n, i in enumerate(result_lst, 1):
        for j in i.values():
            result_txt += f'<code>{str(j).upper():^8}</code>'
        result_txt += '\n'
    # logger.info(result_txt)
    return result_txt, result_lst


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
            if i.TelegramUser_CardUser.telegram_id == msg.from_user.id:
                result_dict['ID'] = i.pk
                result_dict['Имя'] = i.name_card
                result_dict['Номер'] = i.number_card
                result_dict['Баланс'] = i.balans_card
            result_lst += [result_dict.copy()]
    return result_lst