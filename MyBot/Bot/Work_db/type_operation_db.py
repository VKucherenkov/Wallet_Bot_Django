import logging

from aiogram import types
from asgiref.sync import sync_to_async

from Bot.common.global_variable import data_parser
from Bot.models import TypeOperation, CategoryOperation, Recipient

logger = logging.getLogger(__name__)


@sync_to_async
def db_typeoperation_crate(msg=None):
    types = ['Доход', 'Расход', 'Перевод между своими счетами']
    type = TypeOperation.objects.all()
    db_name_all = [i.name_type for i in type]
    # logger.info(f'{db_name_all}')
    if not db_name_all:
        for i in types:
            TypeOperation.objects.update_or_create(name_type=f'{i.lower()}')
            logger.info(
                f'Тип операции: "{i}"\n'
                f'добавлен в базу данных {TypeOperation.objects.get(name_type=i.lower()).datetime_add}')
    else:
        logger.info(f'Таблица "Тип операции" уже была создана')

@sync_to_async
def name_type(message: types.Message) -> str:
    if 'оплата' in message.text.lower() or 'покупка' in message.text.lower() or 'списан' in message.text.lower():
        return 'расход'
    elif 'с карты' in message.text.lower():
        return 'перевод между своими счетами'
    elif 'зачисл' in message.text.lower() or 'аванс' in message.text.lower():
        return 'доход'
    elif 'возвр' in message.text.lower():
        return 'возврат'
    try:
        categoryes_pk = Recipient.objects.get(name_recipient=data_parser['name_recipient']).recipient_id
        type_pk = CategoryOperation.get(pk=categoryes_pk).type_id
    except Exception:
        return
    return TypeOperation.get(pk=type_pk).name_type


@sync_to_async
def get_type_for_keyboard():
    types = [i.name_type for i in TypeOperation.objects.all()]
    return types