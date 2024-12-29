from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import choice_type_kbd, get_recipient_kbd

router = Router(name=__name__)


@router.message(ParserHand.recipient_state, F.text)
async def get_recipient_data(message: types.Message, state: FSMContext):
    await state.update_data(name_recipient=message.text.lower())
    await state.set_state(ParserHand.type_state)
    await message.answer(f'Введите тип операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=choice_type_kbd)


@router.message(ParserHand.recipient_state)
async def get_invalid_recipient_data(message: types.Message,):
    recipient_lst = await get_recipient_db()
    await message.answer(f'Введите корректного получателя платежа',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))