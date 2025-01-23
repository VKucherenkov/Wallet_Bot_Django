import logging
from datetime import datetime
from zoneinfo import ZoneInfo

import pytz

from Bot.Work_db.bank_db import name_bank
from Bot.Work_db.card_work import card_name
from Bot.Work_db.category_operation_db import get_name_category
from Bot.Work_db.type_operation_db import name_type
from Bot.common.global_variable import data_parser

logger = logging.getLogger(__name__)

msg1 = (f'[03.12.2024 в 12:07]\n'
        f'Списание за уведомления об операциях\n'
        f'ПЛАТ.СЧЁТ*7473 01:45 Оплата 40р за уведомления по СберКартам. Следующее списание 03.01.25. '
        f'Баланс: 3714,22р.')

msg2 = (f'[18.12.2024 в 08:31]\n'
        f'Покупка MISHA KOFE_VEN\n'
        f'100 ₽\n'
        f'МИР •• 6522\n'
        f'Баланс: 702062,63₽')


def get_datetime(msg):
    date = msg[msg.index('[') + 1: msg.index('[') + 1 + 10] + ' ' + msg[msg.index(
        ']') + 1 - 6: msg.index(']')]
    year = int(date[6: 10])
    month = int(date[3: 5])
    day = int(date[:2])
    hours = int(date[11: 13])
    minutes = int(date[14:])
    sec = int('0')
    milisec = int('000000')
    # Создание конкретной даты и времени
    specific_time = datetime(year, month, day, hours, minutes, sec, milisec)
    # Указание временной зоны
    timezone = ZoneInfo('Asia/Novosibirsk')
    # Привязка времени к временной зоне
    specific_time_with_tz = specific_time.replace(tzinfo=timezone)
    return specific_time_with_tz


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
        data_parser['name_bank'] = await name_bank(data_parser['number_card'])
        data_parser['amount_operation'] = [i for i in msg.split('\n')][2][:-2].replace(',', '.').replace(' ',
                                                                                                         '').replace(
            '+', '')
        data_parser['balans'] = ''.join([i for i in msg.split('\n')][-1].split()[1:-1]).replace(',', '.')
    data_parser['name_card'] = await card_name(data_parser['number_card'])
    data_parser['name_cat'] = await get_name_category(data_parser['name_recipient'])

    data_parser_txt = '\n'.join([f'<code>{key:<16} - {str(value)}</code>' for key, value in data_parser.items()][1:])
    print(data_parser_txt)
    return data_parser, data_parser_txt
