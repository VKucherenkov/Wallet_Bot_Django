from asgiref.sync import sync_to_async

from Bot.common.global_variable import type_category


def validate_type(message):
    return message.text in [i for i in type_category.keys()]
