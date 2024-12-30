import logging
from asyncio import sleep

from aiogram import Router, F, types

from Bot.keyboard.reply_keybord import del_my_card_kbd, start_kbd

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message(F.text)
async def menu(message: types.Message):
    await message.answer('Не понял что ты написал', reply_markup=del_my_card_kbd)
    await sleep(1)
    await message.answer('Вот меню', reply_markup=start_kbd)
