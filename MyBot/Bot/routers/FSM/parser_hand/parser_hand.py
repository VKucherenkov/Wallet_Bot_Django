import logging

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram.enums import ParseMode

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import start_kbd, get_recipient_kbd

logger = logging.getLogger(__name__)

router = Router(name=__name__)

@router.message(F.text == 'Ручной ввод операции')
async def parser(message: types.Message, state: FSMContext):
    await state.set_state(ParserHand.recipient_state)
    recipient_lst = await get_recipient_db()
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    print('запущен def parser')
    text = (f'😊 Привет <b>{message.chat.first_name}</b> 😊\n'
            f'Введите получателя платежа')
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                                            f'<code>{message.date}\n ------------- \n{message.text}</code>',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text}',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))




