import logging

from aiogram import Router, F, types
from django.conf import settings
from aiogram.enums import ParseMode

from Bot.Midlleware.add_db_user import UserUpdateMiddleware
from Bot.Parser_notification.logik_parser_sms import parser_logic_notification
from Bot.keyboard.reply_keybord import start_kbd

router = Router(name=__name__)


logger = logging.getLogger(__name__)

@router.message(F.text=='Ручной ввод операции')
async def parser(message: types.Message):
    # note_bool = await parser_logic_notification(message)
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    print('запущен def parser')
    text = f'😊 Привет <b>{message.chat.first_name}</b> 😊'
    text_message = (f'😱 Пользователь <b>{message.chat.first_name}</b> с id {message.from_user.id} написал:\n'
                    f'{message.text}')
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'{message.date}\n ------------- \n{text_message}',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text}', parse_mode=ParseMode.HTML)
    await message.answer(f'{text_message}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)