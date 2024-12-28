from Bot.common.global_variable import categoryes


def validate_category(message):
    return message.text in [i.lower() for i in categoryes.keys()]
