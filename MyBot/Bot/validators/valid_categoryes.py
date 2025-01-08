from aiogram import types


def validator_categoryes(message: types.Message) -> bool:
    return True if message.text.isalpha() else False
