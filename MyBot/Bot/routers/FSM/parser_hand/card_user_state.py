from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.bank_db import name_bank
from Bot.Work_db.card_work import card_number, card_name, card_list_for_kb
from Bot.keyboard.reply_keybord import start_kbd, get_bank_kbd, get_prev_cancel_kbd, get_card_kbd
from Bot.validators.valid_card_name import validator_name_card
from Bot.validators.valid_card_number import validator_card_number

router = Router(name=__name__)


@router.message(ParserHand.card_number_state, F.text, F.func(validator_card_number))
async def get_number_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(number_card=message.text)
    if await card_number(message.text):
        await state.update_data(name_card=await card_name(message.text),
                                name_bank=await name_bank(message.text))
        await state.set_state(ParserHand.operation_state)
        await message.answer(f'Введите сумму по операции',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_prev_cancel_kbd())
    else:
        await state.set_state(ParserHand.card_name_state)
        await message.answer(f'Введите имя карты',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_prev_cancel_kbd())


@router.message(ParserHand.card_number_state)
async def get_invalid_number_card(message: types.Message,):
    card_list = await card_list_for_kb(message)
    await message.answer(f'Введите корректный номер карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_card_kbd(card_list))


@router.message(ParserHand.card_name_state, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_card=message.text.lower())
    await state.set_state(ParserHand.bank_state)
    await message.answer(f'Введите наименование банка',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())


@router.message(ParserHand.card_name_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректное имя карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())





