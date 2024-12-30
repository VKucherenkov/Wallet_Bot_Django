import logging
from asyncio import sleep

from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from django.conf import settings

from Bot.FSM_processing.states import ParserAuto, ParserHand
from Bot.keyboard.reply_keybord import start_kbd, del_my_card_kbd


router = Router(name=__name__)

logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def start(message: types.Message):
    logger.info(f'Пользователь: {message.chat.first_name} '
                f'с Telegram id: {message.from_user.id} написал:\n'
                f'{message.text}')
    text = f'😊 Привет <b>{message.chat.first_name}</b> 😊'
    text_message = (f'😱 Пользователь <b>{message.chat.first_name}</b> с id {message.from_user.id} написал:\n'
                    f'{message.text}')
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                                            f'<code>{message.date}\n ------------- \n{message.text}</code>',
                                       parse_mode=ParseMode.HTML)
    await message.answer(f'{text}', parse_mode=ParseMode.HTML)
    await message.answer(f'{text_message}', parse_mode=ParseMode.HTML, reply_markup=start_kbd)


@router.message(Command('menu'))
@router.message(F.text == 'Главное меню')
async def menu(message: types.Message):
    if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
        await message.bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN,
                                       text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                                            f'<code>{message.date}\n ------------- \n{message.text}</code>',
                                       parse_mode=ParseMode.HTML)
    await message.answer('Выходим в главное меню', reply_markup=del_my_card_kbd)
    await sleep(1)
    await message.answer('Вот меню', reply_markup=start_kbd)


@router.message(F.text.lower().contains('отмена'), ParserAuto())
@router.message(F.text.lower().contains('отмена'), ParserHand())
async def cancel_handler(message: types.Message) -> None:
    await message.answer('Вы все отменили, выходим в главное меню', reply_markup=start_kbd)
