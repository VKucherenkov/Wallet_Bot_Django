from decimal import Decimal


from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.keyboard.reply_keybord import start_kbd, get_prev_cancel_kbd
from Bot.validators.valid_operation import validator_operation

router = Router(name=__name__)


@router.message(ParserHand.operation_state_out, F.text, F.func(validator_operation))
async def get_operation(message: types.Message,
                        state: FSMContext):
    operation_out = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    await state.update_data(amount_operation_out=Decimal(operation_out))
    await state.set_state(ParserHand.balance_state_out)
    await message.answer(f'Введите баланс по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.operation_state, F.text, F.func(validator_operation))
async def get_operation(message: types.Message,
                        state: FSMContext):
    operation = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    await state.update_data(amount_operation=Decimal(operation))
    await state.set_state(ParserHand.balance_state)
    await message.answer(f'Введите баланс по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.operation_state_out)
@router.message(ParserHand.operation_state)
async def get_invalid_operation(message: types.Message, ):
    await message.answer(f'Введите корректную сумму по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())
