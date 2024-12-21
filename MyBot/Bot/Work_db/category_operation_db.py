import logging

from aiogram import types
from asgiref.sync import sync_to_async

from Bot.common.global_variable import categoryes, type_category, data_parser
from Bot.models import CategoryOperation, TypeOperation, Recipient

logger = logging.getLogger(__name__)


@sync_to_async
def db_categoryoperation_create():
    cat = [i for i in categoryes.keys()]
    cat_obj = CategoryOperation.objects.all()
    typeoperation = [(i, j) for i in cat for j, value in type_category.items() if i in value]
    db_name_all = [i.name_cat for i in cat_obj]
    # logger.info(f'{db_name_all}')
    # logger.info(f'{typeoperation}')
    if not db_name_all:
        for i, j in typeoperation:
            pk = TypeOperation.objects.get(name_type=j).pk
            CategoryOperation.objects.update_or_create(name_cat=f'{i}', TypeOperation_CategoryOperation_id=pk)
            logger.info(
                f'Категория операции: "{i}"\n'
                f'Тип операции: "{j}"\n'
                f'добавлен в базу данных {CategoryOperation.objects.get(name_cat=i).datetime_add}')
    else:
        logger.info(f'Таблица "Категория операции" уже была создана')

@sync_to_async
def name_cat(message: types.Message) -> str:
    try:
        categoryes_pk = Recipient.objects.get(name_recipient=data_parser['name_recipient']).Recipient_CategoryOperation_id
    except Exception:
        return
    return CategoryOperation.get(pk=categoryes_pk).name_cat