import datetime
from decimal import Decimal

import pytz
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.load_db_operation import load_db_operaion
from Bot.keyboard.reply_keybord import start_kbd, get_prev_cancel_kbd
from Bot.validators.valid_balance import validator_balance

router = Router(name=__name__)


@router.message(ParserHand.balance_state, F.text, F.func(validator_balance))
async def get_balance(message: types.Message,
                        state: FSMContext):
    tz = pytz.timezone("Asia/Novosibirsk")
    balance = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    data = await state.update_data(balans=Decimal(balance), datetime_amount=datetime.datetime.now(tz), telegram_id=message.from_user.id)
    await state.clear()
    await message.answer(f'Проверьте правильность введенной операции.',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)
    await resume_input_notification(message=message, data=data)


@router.message(ParserHand.balance_state)
async def get_invalid_balance(message: types.Message,):
    await message.answer(f'Введите корректный баланс по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


async def resume_input_notification(message: types.Message, data):
    text = ''
    for key, value in data.items():
        text += f'{key}------{value}\n'
    result = await load_db_operaion(data)
    if type(result) == int:
        text += 'Данные по операции записаны в базу данных.' + '\n' + f'ID операции:  {result}'
    else:
        text += 'Данные по операции не записаны в базу данных.' + '\n' + f'{result}'
    await message.answer(text=text)