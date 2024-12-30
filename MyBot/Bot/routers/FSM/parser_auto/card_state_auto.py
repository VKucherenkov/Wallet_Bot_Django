from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import get_bank_kbd, get_prev_cancel_kbd, get_recipient_kbd
from Bot.validators.valid_bank import validator_bank
from Bot.validators.valid_card_name import validator_name_card

router = Router(name=__name__)

@router.message(ParserAuto.card_name_state, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_card=message.text.lower())
    await state.set_state(ParserAuto.bank_state)
    await message.answer(f'Введите наименование банка или выберете из предложенных ниже',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())


@router.message(ParserAuto.card_name_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректное имя карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserAuto.bank_state, F.text, F.func(validator_bank))
async def get_name_bank(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_bank=message.text.lower())
    data = await state.update_data()
    recipient_lst = await get_recipient_db()
    if data['name_recipient'] not in recipient_lst:
        await state.set_state(ParserAuto.recipient_state)
        await message.answer(f'Введите получателя платежа или выберете из списка ниже',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))

@router.message(ParserAuto.bank_state)
async def get_invalid_name_bank(message: types.Message, ):
    await message.answer(f'Введите корректный банк',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())