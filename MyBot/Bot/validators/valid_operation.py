from aiogram import types


def validator_operation(message: types.Message) -> bool:
    operation = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    if '.' not in operation:
        operation += '.00'
    return True if len(operation.split('.')) <= 2 and all([i.isdigit() for i in operation.split('.')]) and len(
        operation.split('.')[1]) == 2 else False
