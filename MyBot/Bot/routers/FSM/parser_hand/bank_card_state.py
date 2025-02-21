from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.keyboard.reply_keybord import get_prev_cancel_kbd, get_bank_kbd
from Bot.validators.valid_bank import validator_bank

router = Router(name=__name__)


@router.message(ParserHand.bank_state_out, F.text, F.func(validator_bank))
async def get_name_bank(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_bank_out=message.text.lower())
    await state.set_state(ParserHand.operation_state_out)
    await message.answer(f'Введите сумму по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.bank_state, F.text, F.func(validator_bank))
async def get_name_bank(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_bank=message.text.lower())
    await state.set_state(ParserHand.operation_state)
    await message.answer(f'Введите сумму по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.bank_state_out)
@router.message(ParserHand.bank_state)
async def get_invalid_name_bank(message: types.Message, ):
    await message.answer(f'Введите корректный банк',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())
