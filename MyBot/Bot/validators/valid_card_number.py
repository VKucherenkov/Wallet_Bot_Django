from aiogram import types


def validator_card_number(message: types.Message) -> bool:
    return True if message.text.isdigit() and len(message.text) == 4 else False