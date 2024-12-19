import logging

from asgiref.sync import sync_to_async

from Bot.models import TypeOperation

logger = logging.getLogger(__name__)


# @sync_to_async
def db_typeoperation(msg=None):
    types = ['Доход', 'Расход', 'Перевод между своими счетами']
    type = TypeOperation.objects.all()
    db_name_all = [i.name_type for i in type]
    logger.info(f'{db_name_all}')
    if not db_name_all:
        for i in types:
            TypeOperation.objects.update_or_create(name_type=f'{i}')
            logger.info(
                f'Тип операции: "{i}"\n'
                f'добавлен в базу данных {TypeOperation.objects.get(name_type=i).datetime_add}')
    else:
        logger.info(f'Таблица "Тип операции" уже была создана')