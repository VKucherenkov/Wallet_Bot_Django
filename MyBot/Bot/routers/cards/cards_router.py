import logging

from aiogram import Router, F, types

from Bot.Work_db.card_work import card_list
from Bot.keyboard.reply_keybord import my_card_kbd

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.text =='Мои карты')
async def card_support(message: types.Message):
    card_lst = await card_list(message)
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    if card_lst:
        await message.answer(f'Вот Ваши карты:\n{card_lst}', reply_markup=my_card_kbd)
        await message.answer('Выберете что надо сделать с картами')
    else:
        await message.answer(f'У Вас нет активных карт', reply_markup=my_card_kbd)
        await message.answer('Выберете что надо сделать с картами')
