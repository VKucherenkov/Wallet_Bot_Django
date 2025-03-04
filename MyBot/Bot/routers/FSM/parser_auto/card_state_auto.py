from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.category_operation_db import get_name_category_auto, get_categories_for_keyboard
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import get_bank_kbd, get_prev_cancel_kbd, get_recipient_kbd, get_category_kbd, \
    get_yes_no_kbd, get_card_type_kbd, get_currency_kbd
from Bot.validators.valid_bank import validator_bank
from Bot.validators.valid_card_name import validator_name_card, validator_type_card, validator_limit_card, \
    validator_currency_card

router = Router(name=__name__)

@router.message(ParserAuto.card_name_state, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_card=message.text.lower())
    await state.set_state(ParserAuto.card_currency_state)
    await message.answer(f'Введите валюту карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_currency_kbd())


@router.message(ParserAuto.card_name_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректное имя карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserAuto.card_currency_state, F.text, F.func(validator_currency_card))
async def get_currency_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(currency_card=message.text.lower())
    await state.set_state(ParserAuto.card_type_state)
    await message.answer(f'Введите тип карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_card_type_kbd())


@router.message(ParserAuto.card_currency_state)
async def get_invalid_currency_card(message: types.Message,):
    await message.answer(f'Введите корректную валюту карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_currency_kbd())


@router.message(ParserAuto.card_type_state, F.text, F.func(validator_type_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(type_card=message.text.lower())
    if message.text.lower() == 'дебетовая':
        await state.update_data(credit_limit=0)
        await state.set_state(ParserAuto.bank_state_auto)
        await message.answer(f'Введите наименование банка или выберете из предложенных ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_bank_kbd())
    else:
        await state.set_state(ParserAuto.card_credit_state)
        await message.answer(f'Введите кредитный лимит по карте',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_prev_cancel_kbd())


@router.message(ParserAuto.card_type_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректный тип карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_card_type_kbd()())


@router.message(ParserAuto.card_credit_state, F.text, F.func(validator_limit_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(credit_limit=message.text)
    await state.set_state(ParserAuto.bank_state_auto)
    await message.answer(f'Введите наименование банка или выберете из предложенных ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_bank_kbd())


@router.message(ParserAuto.card_credit_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректный лимит по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_prev_cancel_kbd())


@router.message(ParserAuto.bank_state_auto, F.text, F.func(validator_bank))
async def get_name_bank(message: types.Message,
                        state: FSMContext):
    data = await state.update_data(name_bank=message.text.lower())
    recipient_lst = await get_recipient_db()
    category_lst = await get_name_category_auto(data['name_recipient'])
    if data['name_recipient'] not in recipient_lst:
        await state.set_state(ParserAuto.recipient_state)
        recipient_lst += [data['name_recipient']]
        await message.answer(f'Введите получателя платежа или выберете из списка ниже',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))
    elif len(category_lst) != 1:
        await state.set_state(ParserAuto.category_state_auto)
        category_lst = await get_categories_for_keyboard()
        await message.answer(f'Введите категорию операции или выберете из списка ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_category_kbd(category_lst))
    else:
        data = await state.update_data(name_cat=category_lst[0])
        text = ''
        for key, value in data.items():
            text += f'<code>{key:<17} ------ {value}</code>\n'
        await state.set_state(ParserAuto.resume_state)
        await message.answer(text=text,
                             parse_mode=ParseMode.HTML)
        await message.answer(f'Проверьте и подтвердите правильность введенных данных по операции',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_yes_no_kbd())

@router.message(ParserAuto.bank_state_auto)
async def get_invalid_name_bank(message: types.Message, ):
    await message.answer(f'Введите корректный банк',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())