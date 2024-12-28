from aiogram import types


def validator_bank(message: types.Message) -> bool:
    return False if message.text.isdigit() else True