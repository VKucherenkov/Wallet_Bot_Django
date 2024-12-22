import logging


from Bot.Work_db.bank_db import name_bank
from Bot.Work_db.card_work import card_name
from Bot.Work_db.category_operation_db import name_cat
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


async def parser_logic_notification(message):
    msg = message.text
    data_parser['note_operation'] = msg
    data_parser['datetime_amount'] = msg[msg.index('[') + 1: msg.index('[') + 1 + 10] + ' ' + msg[msg.index(
        ']') + 1 - 6: msg.index(']')]
    data_parser['name_type'] = await name_type(message)
    data_parser['name_cat'] = await name_cat(message)
    data_parser['recipient_in_notification'] = [i for i in msg.split('\n')][1]
    if 'списание' in [i.lower() for i in msg.split('\n')][1]:
        data_parser['number_card'] = msg[msg.index('*') + 1: msg.index('*') + 1 + 4]
        data_parser['name_bank'] = 'Сбербанк'
        data_parser['name_recipient'] = 'Сбербанк'
        data_parser['amount_operation'] = [j[:-1] for j in [i for i in msg.split('\n')][2].split() if j[-1] == 'р'][0]
        data_parser['balans'] = [i for i in msg.split('\n')][-1].split()[-1][:-2].replace(',', '.')

    elif 'покупка' in [i.lower() for i in msg.split('\n')][1]:
        data_parser['number_card'] = msg[msg.rindex('•') + 2: msg.index('•') + 2 + 5]
        data_parser['name_recipient'] = ' '.join([i for i in msg.split('\n')][1].split()[1:])
        data_parser['name_bank'] = await name_bank()
        data_parser['amount_operation'] = [i for i in msg.split('\n')][2][:-2].replace(',', '.').replace(' ', '')
        data_parser['balans'] = ''.join([i for i in msg.split('\n')][-1].split()[1:-1]).replace(',', '.')
    data_parser['name_card'] = await card_name(data_parser['number_card'])

    [print(f'{key} ------ {value}') for key, value in data_parser.items()]
    return (all([i for i in data_parser.values()]))
