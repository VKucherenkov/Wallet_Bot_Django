from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import get_recipient_kbd, get_prev_cancel_kbd

router = Router(name=__name__)


@router.message(ParserHand.recipient_state, F.text)
async def get_recipient_data(message: types.Message, state: FSMContext):
    await state.update_data(name_recipient=message.text.lower())
    await state.set_state(ParserHand.date_amount_state)
    await message.answer(f'Введите дату операции в формате "день, месяц, год, час, минуты". '
                         f'Например для даты 1 января 2025 года 9:05 часов, следует ввести: 1, 1, 2025, 9, 5.',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.recipient_state)
async def get_invalid_recipient_data(message: types.Message,):
    recipient_lst = await get_recipient_db()
    await message.answer(f'Введите корректного получателя платежа',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))