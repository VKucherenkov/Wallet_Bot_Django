import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import pytz

from Bot.Work_db.bank_db import get_bank_name_by_card
from Bot.Work_db.card_work import card_name
from Bot.Work_db.category_operation_db import get_name_category_auto, get_name_category
from Bot.Work_db.type_operation_db import name_type


logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)


def get_datetime(msg: str) -> datetime:
    """
    Извлекает дату и время из строки сообщения и возвращает объект datetime с временной зоной.

    :param msg: Строка сообщения.
    :return: Объект datetime с временной зоной.
    :raises ValueError: Если формат строки не соответствует ожидаемому.
    """
    try:
        # Извлекаем дату и время из строки
        date_str = msg[msg.index('[') + 1: msg.index('[') + 1 + 10]
        time_str = msg[msg.index(']') + 1 - 6: msg.index(']')]

        # Разбираем дату и время
        day, month, year = map(int, date_str.split('.'))
        hours, minutes = map(int, time_str.split(':'))

        # Создаем объект datetime
        specific_time = datetime(year, month, day, hours, minutes, 0, 0)

        # Привязываем к временной зоне
        timezone = ZoneInfo('Asia/Novosibirsk')
        specific_time_with_tz = specific_time.replace(tzinfo=timezone)

        logger.info(f"Успешно извлечена дата и время: {specific_time_with_tz}")
        return specific_time_with_tz

    except (ValueError, IndexError) as err:
        # Логируем ошибку
        logger.error(f"Ошибка при извлечении даты и времени из строки: {msg}. Ошибка: {err}", exc_info=True)
        raise ValueError(f"Некорректный формат строки: {msg}") from err


async def parser_logic_notification(message):
    msg = message.text
    data_parser = {}
    data_parser['note_operation'] = msg
    data_parser['datetime_amount'] = get_datetime(msg)
    data_parser['name_type'] = await name_type(message)

    data_parser['recipient_in_notification'] = [i for i in msg.split('\n')][1]
    if 'списание' in [i.lower() for i in msg.split('\n')][1]:
        data_parser['number_card'] = msg[msg.index('*') + 1: msg.index('*') + 1 + 4]
        if data_parser['number_card'] == '7473':
            data_parser['number_card'] = '8314'
        data_parser['name_bank'] = 'Сбербанк'
        data_parser['name_recipient'] = 'Сбербанк'
        data_parser['amount_operation'] = [j[:-1] for j in [i for i in msg.split('\n')][2].split() if j[-1] == 'р'][0]
        data_parser['balans'] = [i for i in msg.split('\n')][-1].split()[-1][:-2].replace(',', '.')

    elif 'покупка' in [i.lower() for i in msg.split('\n')][1] or 'зачислен' in [i.lower() for i in msg.split('\n')][
        1] or 'оплата' in [i.lower() for i in msg.split('\n')][1] or 'возвр' in [i.lower() for i in msg.split('\n')][
        1] or 'перевод от' in [i.lower() for i in msg.split('\n')][1] or 'перевод' in \
            [i.lower() for i in msg.split('\n')][1]:
        data_parser['number_card'] = msg[msg.rindex('•') + 2: msg.index('•') + 2 + 5]
        if data_parser['number_card'] == '7473':
            data_parser['number_card'] = '8314'
        data_parser['name_recipient'] = ' '.join([i for i in msg.split('\n')][1].split()[1:])
        data_parser['name_bank'] = await get_bank_name_by_card(data_parser['number_card'])
        data_parser['amount_operation'] = [i for i in msg.split('\n')][2][:-2].replace(',', '.').replace(' ',
                                                                                                         '').replace(
            '+', '')
        data_parser['balans'] = ''.join([i for i in msg.split('\n')][-1].split()[1:-1]).replace(',', '.')
    data_parser['name_card'] = await card_name(data_parser['number_card'])
    data_parser['name_cat'] = await get_name_category(data_parser['name_recipient'])

    data_parser_txt = '\n'.join([f'<code>{key:<16} - {str(value)}</code>' for key, value in data_parser.items()][1:])
    print(data_parser_txt)
    return data_parser, data_parser_txt