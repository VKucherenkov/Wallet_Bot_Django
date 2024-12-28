from aiogram import types

from Bot.Work_db.card_work import card_name


def validator_balance(message: types.Message) -> bool:
    balance_notification = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    if '.' not in balance_notification:
        balance_notification += '.00'
    return True if len(balance_notification.split('.')) <= 2 and all(
        [i.isdigit() for i in balance_notification.split('.')]) and len(
        balance_notification.split('.')[1]) == 2 else False
