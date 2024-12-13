
from Bot.models import TelegramUser


def db_telegramuser(msg, logger):
    w = TelegramUser.objects.all()
    db_id_all = [i.telegram_id for i in w]
    logger.info(f'{db_id_all}')
    logger.info(f'{msg.from_user.id}')
    logger.info(f'{msg.chat.first_name}')
    logger.info(f'{msg.chat.last_name}')
    if not msg.from_user.id in db_id_all:
        TelegramUser.objects.create(telegram_id=f'{msg.from_user.id}',
                                    first_name=f'{msg.chat.first_name}',
                                    last_name=f'{msg.chat.last_name}')
    return True
