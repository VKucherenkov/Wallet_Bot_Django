import datetime
import logging
from decimal import Decimal

import pytz
from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.card_work import card_list_for_kb
from Bot.Work_db.load_db_operation import load_db_operation
from Bot.keyboard.reply_keybord import start_kbd, get_prev_cancel_kbd, get_card_kbd
from Bot.validators.valid_balance import validator_balance

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message(ParserHand.balance_state_out, F.text, F.func(validator_balance))
async def get_balance(message: types.Message,
                        state: FSMContext):
    tz = pytz.timezone("Asia/Novosibirsk")
    balance_out = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    await state.update_data(balans_out=Decimal(balance_out), telegram_id_out=message.from_user.id)
    await state.set_state(ParserHand.card_number_state)
    card_list = await card_list_for_kb(message)
    await message.answer(f'Введите номер новой карты для зачисления денежных средств,'
                         f' или выберите из предложенных ниже',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_card_kbd(card_list))


@router.message(ParserHand.balance_state, F.text, F.func(validator_balance))
async def get_balance(message: types.Message,
                        state: FSMContext):
    tz = pytz.timezone("Asia/Novosibirsk")
    balance = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    data = await state.update_data(balans=Decimal(balance), telegram_id=message.from_user.id)
    await state.clear()
    await message.answer(f'Проверьте правильность введенной операции.',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)
    await resume_input_notification(message=message, data=data)


@router.message(ParserHand.balance_state_out)
@router.message(ParserHand.balance_state)
async def get_invalid_balance(message: types.Message,):
    await message.answer(f'Введите корректный баланс по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


async def resume_input_notification(message: types.Message, data):
    try:
        result, text = await load_db_operation(data)
    except Exception as err:
        logger.error(f"Произошла ошибка при обработке операции: {err}", exc_info=True)
        return err
    if type(result) in [str]:
        text += '\n<code>Данные по операции записаны в базу данных.' + '\n' + f'ID операции:  {result}</code>'
    else:
        text += '\n<code>Данные по операции не записаны в базу данных.' + '\n' + f'{result}</code>'
    await message.answer(text=text, parse_mode=ParseMode.HTML)