import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import types

from Bot.Work_db.bank_db import get_bank_name_by_card
from Bot.Work_db.card_work import card_name, get_type_card, get_credit_limit_card
from Bot.Work_db.category_operation_db import get_name_category_auto, get_name_category
from Bot.Work_db.type_operation_db import name_type


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


async def parser_logic_notification(message: types.Message):
    msg = message.text
    data_parser = {
        'note_operation': msg,
        'datetime_amount': get_datetime(msg),
        'name_type': await name_type(message),
    }

    lines = [line.strip() for line in msg.split('\n') if line.strip()]
    if len(lines) < 2:
        raise ValueError("Недостаточно данных в сообщении для парсинга.")

    data_parser['recipient_in_notification'] = lines[1]

    # Обработка списания
    if 'списание' in lines[1].lower():
        await parse_withdrawal(data_parser, msg, lines)

    # Обработка покупки, зачисления, перевода и т.д.
    elif any(keyword in lines[1].lower() for keyword in ['покупка', 'капитал', 'зачислен', 'оплата', 'возвр', 'перевод от', 'перевод']):
        await parse_income_or_payment(data_parser, msg, lines)

    # Дополнительные данные
    data_parser['name_card'] = await card_name(data_parser['number_card'])
    data_parser['name_cat'] = await get_name_category(data_parser['name_recipient'])
    data_parser['type_card'] = await get_type_card(data_parser['number_card']) if data_parser['name_card'] else None
    data_parser['credit_limit'] = await get_credit_limit_card(data_parser['number_card']) if data_parser['name_card'] else None

    # Форматирование данных для вывода
    data_parser_txt = '\n'.join([f'<code>{key:<16} - {str(value)}</code>' for key, value in data_parser.items()][1:])
    return data_parser, data_parser_txt


async def parse_withdrawal(data_parser, msg, lines):
    """Обработка списания."""
    data_parser['number_card'] = extract_card_number(msg, '*', 4)
    if data_parser['number_card'] == '8314':
        data_parser['number_card'] = '7473'
    data_parser['name_bank'] = 'Сбербанк'
    data_parser['name_recipient'] = 'Сбербанк'
    data_parser['amount_operation'] = extract_amount(lines[2], 'р')
    data_parser['balans'] = extract_balance(lines[-1])


async def parse_income_or_payment(data_parser, msg, lines):
    """Обработка зачислений, покупок, переводов и т.д."""
    data_parser['number_card'] = extract_card_number_buy(msg, '•', 4)
    if data_parser['number_card'] == '8314':
        data_parser['number_card'] = '7473'
    data_parser['name_recipient'] = ' '.join(lines[1].split()[1:])
    data_parser['name_bank'] = await get_bank_name_by_card(data_parser['number_card'])
    # data_parser['amount_operation'] = lines[2][:-2].replace(',', '.').replace(' ', '').replace('+', '')
    data_parser['amount_operation'] = ''.join(lines[2].split()[:-1]).replace(',', '.')
    data_parser['balans'] = ''.join(lines[-1].split()[1:-1]).replace(',', '.')


def extract_card_number(msg, symbol, length):
    """Извлечение номера карты."""
    try:
        return msg[msg.rindex(symbol) + 1: msg.rindex(symbol) + 1 + length]
    except ValueError:
        return "Неизвестно"


def extract_card_number_buy(msg, symbol, length):
    """Извлечение номера карты."""
    try:
        return msg[msg.rindex(symbol) + 2: msg.rindex(symbol) + 2 + length]
    except ValueError:
        return "Неизвестно"


def extract_amount(line, currency_symbol):
    """Извлечение суммы операции."""
    for part in line.split():
        if part.endswith(currency_symbol):
            return part[:-1]
    return "Неизвестно"


def extract_balance(line):
    """Извлечение баланса."""
    return line.split()[-1][:-2].replace(',', '.')