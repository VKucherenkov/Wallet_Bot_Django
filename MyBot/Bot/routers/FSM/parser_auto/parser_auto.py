import logging

from aiogram import types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram import F

from Bot.FSM_processing.states import ParserAuto
from Bot.Parser_notification.logik_parser_sms import parser_logic_notification
from Bot.keyboard.reply_keybord import start_kbd

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.text =='Ввод типичной операции')
async def start_auto_parser(message: types.Message, state: FSMContext):
    await state.set_state(ParserAuto.recipient_state)
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    text_message = 'В поле ввода текста вставьте уведомление полученное из банка'
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'{message.date}\n ------------- \n{text_message}',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text_message}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)


@router.message(ParserAuto.recipient_state, F.text.lower().contains(']'), F.text.lower().contains('['))
async def recipient_auto_parser(message: types.Message, state: FSMContext):
    data, data_txt = await parser_logic_notification(message)
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'{message.date}\n ------------- \n{message.text}',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{data_txt}', parse_mode=ParseMode.HTML)
    await message.answer(f'{"принят"}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)


