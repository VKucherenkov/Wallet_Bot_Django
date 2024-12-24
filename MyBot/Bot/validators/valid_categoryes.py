from aiogram import types


def validator_categoryes(message: types.Message) -> bool:
    return False if message.text.isdigit() else True
