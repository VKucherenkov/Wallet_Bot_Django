from aiogram import types


def validator_categoryes(message: types.Message) -> bool:
    return len(message.text) > 1
