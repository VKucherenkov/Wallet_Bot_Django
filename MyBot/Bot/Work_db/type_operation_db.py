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
            TypeOperation.objects.update_or_create(name_type=f'{i}')
            logger.info(
                f'Тип операции: "{i}"\n'
                f'добавлен в базу данных {TypeOperation.objects.get(name_type=i).datetime_add}')
    else:
        logger.info(f'Таблица "Тип операции" уже была создана')

@sync_to_async
def name_type(message: types.Message) -> str:
    try:
        categoryes_pk = Recipient.objects.get(name_recipient=data_parser['name_recipient']).Recipient_CategoryOperation_id
        type_pk = CategoryOperation.get(pk=categoryes_pk).TypeOperation_CategoryOperation_id
    except Exception:
        return
    return TypeOperation.get(pk=type_pk).name_type