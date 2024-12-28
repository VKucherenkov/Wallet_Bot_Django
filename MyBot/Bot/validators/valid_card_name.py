from aiogram import types


def validator_name_card(message: types.Message) -> bool:
    return False if message.text.isdigit() else True