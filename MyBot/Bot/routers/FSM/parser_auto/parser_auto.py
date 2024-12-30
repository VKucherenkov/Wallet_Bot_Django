import logging

from aiogram import types, Router
from aiogram.enums import ParseMode

from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram import F

from Bot.FSM_processing.states import ParserAuto
from Bot.Parser_notification.logik_parser_sms import parser_logic_notification
from Bot.Work_db.card_work import card_list, card_number
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import start_kbd, get_prev_cancel_kbd, get_recipient_kbd

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.text =='Ввод типичной операции')
async def start_auto_parser(message: types.Message,
                            state: FSMContext):
    await state.set_state(ParserAuto.start_state)
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    text_message = 'В поле ввода текста вставьте уведомление полученное из банка'
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                                            f'<code>{message.date}\n ------------- \n{message.text}</code>',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text_message}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)


@router.message(ParserAuto.start_state, F.text.lower().contains('['))
async def recipient_auto_parser(message: types.Message, state: FSMContext):
    data, data_txt = await parser_logic_notification(message)
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                                            f'<code>{message.date}\n ------------- \n{message.text}</code>',
                                       parse_mode=ParseMode.HTML)
    logger.info(data)
    await state.update_data(number_card=data['number_card'],
                            name_card=data['name_card'],
                            name_bank=data['name_bank'],
                            balans=data['balans'],
                            amount_operation=data['amount_operation'],
                            name_recipient=data['name_recipient'],
                            recipient_in_notification=data['recipient_in_notification'],
                            name_cat=data['name_cat'],
                            name_type=data['name_type'],
                            datetime_amount=data['datetime_amount'],
                            note_operation=data['note_operation'])
    await message.answer(f'{data_txt}', parse_mode=ParseMode.HTML)
    await message.answer(f'{"принят"}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)
    card_num = await card_number(data['number_card'])
    recipient_lst = await get_recipient_db()
    if not card_num:
        await state.set_state(ParserAuto.card_name_state)
        await message.answer(f'{"Введите имя карты"}', parse_mode=ParseMode.HTML, reply_markup=get_prev_cancel_kbd())
    # elif data['name_recipient'] not in recipient_lst:
    #     await state.set_state(ParserAuto.recipient_state)
    #     await message.answer(f'Введите получателя платежа или выберете из списка ниже',
    #                          parse_mode=ParseMode.HTML,
    #                          reply_markup=get_recipient_kbd(recipient_lst))




