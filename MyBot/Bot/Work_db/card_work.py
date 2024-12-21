import logging
from pyexpat.errors import messages

from aiogram import types
from asgiref.sync import sync_to_async

from Bot.common.global_variable import data_parser
from Bot.models import CardUser

logger = logging.getLogger(__name__)


@sync_to_async
def card_list(msg):
    cards = CardUser.objects.all()
    result = ''
    if cards:
        for i in cards:
           if i.TelegramUser_CardUser.telegram_id == msg.from_user.id:
               result += f'{i.pk:<20}{i.name_card:<20}{i.number_card:<10}{i.balans_card:>20}\n'
    return result

@sync_to_async
def card_name(message: types.Message) -> str:
    cards = CardUser.objects.all()
    try:
        card_name = cards.get(number_card=data_parser['number_card']).card_name
    except Exception:
        return
    return card_name
