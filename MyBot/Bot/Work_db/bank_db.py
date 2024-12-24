import logging

from asgiref.sync import sync_to_async

from Bot.common.global_variable import banks, data_parser
from Bot.models import BankCard, CardUser

logger = logging.getLogger(__name__)


@sync_to_async
def db_bank_create(msg=None):
    bank = [i for i in banks.keys()]
    bank_obj = BankCard.objects.all()
    db_name_all = [i.name_bank for i in bank_obj]
    # logger.info(f'{db_name_all}')
    # logger.info(f'{typeoperation}')
    if not db_name_all:
        for i in bank:
            BankCard.objects.update_or_create(name_bank=f'{i.lower()}')
            logger.info(
                f'Наименование банка: "{i}"\n'
                f'добавлен в базу данных {BankCard.objects.get(name_bank=i.lower()).datetime_add}')
    else:
        logger.info(f'Таблица "Банки" уже была создана')


@sync_to_async
def name_bank():
    try:
        bank_pk = CardUser.objects.get(number_card=data_parser['number_card']).BankCard_CardUser_id
    except Exception as err:
        logger.info(err)
        return
    return BankCard.objects.get(pk=bank_pk).name_bank