import datetime
import logging
from decimal import Decimal

import pytz

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram.enums import ParseMode

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.load_db_operation import load_db_operaion
from Bot.common.global_variable import type_category
from Bot.keyboard.reply_keybord import start_kbd, choice_type_kbd, get_category_kbd, get_bank_kbd
from Bot.validators.valid_balance import validator_balance
from Bot.validators.valid_bank import validator_bank
from Bot.validators.valid_card_name import validator_name_card
from Bot.validators.valid_card_number import validator_card_number
from Bot.validators.valid_categoryes import validator_categoryes
from Bot.validators.valid_operation import validator_operation
from Bot.validators.validator_type import validate_type

router = Router(name=__name__)


logger = logging.getLogger(__name__)

@router.message(F.text=='Ручной ввод операции')
async def parser(message: types.Message, state: FSMContext):
    await state.set_state(ParserHand.recipient_state)
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    print('запущен def parser')
    text = (f'😊 Привет <b>{message.chat.first_name}</b> 😊\n'
            f'Введи получателя платежа')
    text_message = (f'😱 Пользователь <b>{message.chat.first_name}</b> с id {message.from_user.id} написал:\n'
                    f'{message.text}')
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'{message.date}\n ------------- \n{text_message}',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text}',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.recipient_state, F.text)
async def get_recipient_data(message: types.Message, state: FSMContext):
    await state.update_data(name_recipient=message.text.lower())
    await state.set_state(ParserHand.type_state)
    await message.answer(f'Введите тип операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=choice_type_kbd)


@router.message(ParserHand.recipient_state)
async def get_invalid_recipient_data(message: types.Message,):
    await message.answer(f'Введите корректного получателя платежа',
                         parse_mode=ParseMode.HTML)

@router.message(ParserHand.type_state,
                F.text, F.func(validate_type))
async def get_name_type(message: types.Message,
                             state: FSMContext):
    await state.update_data(name_type=message.text.lower())
    await state.set_state(ParserHand.category_state)
    await message.answer(f'Введите категорию операции',
                         parse_mode=ParseMode.HTML, reply_markup=get_category_kbd())


@router.message(ParserHand.type_state)
async def get_invalid_name_type(message: types.Message,):
    await message.answer(f'Введите корректный тип операции',
                         parse_mode=ParseMode.HTML)


@router.message(ParserHand.category_state, F.text, F.func(validator_categoryes))
async def get_name_category(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_cat=message.text.lower())
    await state.set_state(ParserHand.bank_state)
    await message.answer(f'Введите банк эмитента карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_bank_kbd())


@router.message(ParserHand.category_state)
async def get_invalid_name_category(message: types.Message,):
    await message.answer(f'Введите корректную категорию операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.bank_state, F.text, F.func(validator_bank))
async def get_name_bank(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_bank=message.text.lower())
    await state.set_state(ParserHand.card_name_state)
    await message.answer(f'Введите имя карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.bank_state)
async def get_invalid_name_bank(message: types.Message,):
    await message.answer(f'Введите корректный банк',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.card_name_state, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_card=message.text.lower())
    await state.set_state(ParserHand.card_number_state)
    await message.answer(f'Введите номер карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.card_name_state)
async def get_invalid_name_card(message: types.Message,):
    await message.answer(f'Введите корректное имя карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.card_number_state, F.text, F.func(validator_card_number))
async def get_number_card(message: types.Message,
                        state: FSMContext):
    await state.update_data(number_card=message.text)
    await state.set_state(ParserHand.operation_state)
    await message.answer(f'Введите сумму по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.card_number_state)
async def get_invalid_number_card(message: types.Message,):
    await message.answer(f'Введите корректный номер карты',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.operation_state, F.text, F.func(validator_operation))
async def get_operation(message: types.Message,
                        state: FSMContext):
    operation = message.text.replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    await state.update_data(amount_operation=Decimal(operation))
    await state.set_state(ParserHand.balance_state)
    await message.answer(f'Введите баланс по карте',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)


@router.message(ParserHand.operation_state)
async def get_invalid_operation(message: types.Message,):
    await message.answer(f'Введите корректную сумму по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=start_kbd)



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
                         reply_markup=start_kbd)

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