import logging

from asgiref.sync import sync_to_async

from Bot.models import TelegramUser

logger = logging.getLogger(__name__)


@sync_to_async
def db_telegramuser(msg):
    w = TelegramUser.objects.all()
    db_id_all = [i.telegram_id for i in w]
    logger.info(f'{db_id_all}')
    logger.info(f'{msg.from_user.id}')
    logger.info(f'{msg.chat.first_name}')
    logger.info(f'{msg.chat.last_name}')
    if not msg.from_user.id in db_id_all:
        TelegramUser.objects.update_or_create(telegram_id=f'{msg.from_user.id}',
                                              first_name=f'{msg.chat.first_name}',
                                              last_name=f'{msg.chat.last_name}')
        logger.info(f'Пользователь {msg.from_user.id} {msg.chat.first_name} {msg.chat.last_name} добавлен в базу данных')
    else:
        user = TelegramUser.objects.get(telegram_id=f'{msg.from_user.id}')
        TelegramUser.objects.filter(telegram_id=f'{msg.from_user.id}').update(
            first_name=f'{user.first_name}',
            last_name=f'{user.last_name}'
        )
        logger.info(
            f'Данные пользователя {msg.from_user.id} {msg.chat.first_name} {msg.chat.last_name} обновлены в базе данных')
