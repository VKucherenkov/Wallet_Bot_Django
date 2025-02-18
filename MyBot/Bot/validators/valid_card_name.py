from aiogram import types

from Bot.common.global_variable import card_type


def validator_name_card(message: types.Message) -> bool:
    return False if message.text.isdigit() else True


def validator_type_card(message: types.Message) -> bool:
    return False if message.text not in [i for i in card_type.values()] else True


def validator_limit_card(message: types.Message) -> bool:
    return False if not message.text.isdigit() else True