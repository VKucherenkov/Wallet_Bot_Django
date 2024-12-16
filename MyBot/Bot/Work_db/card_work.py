import logging

from asgiref.sync import sync_to_async

from Bot.models import CardUser

logger = logging.getLogger(__name__)

c = CardUser.objects.all()

@sync_to_async
def card_list(msg):
    result = ''
    for i in c:
       if i.TelegramUser_CardUser.telegram_id == msg.from_user.id:
           result += f'{i.pk:<20}{i.title:<20}{i.number_card:<10}{i.balans_card:>20}\n'

    return result
