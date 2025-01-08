from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.category_operation_db import get_name_category_auto
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.keyboard.reply_keybord import get_recipient_kbd, get_category_kbd, get_yes_no_kbd

router = Router(name=__name__)


@router.message(ParserAuto.recipient_state, F.text)
async def get_recipient_data(message: types.Message, state: FSMContext):
    data = await state.update_data(name_recipient=message.text.lower())
    category_lst = await get_name_category_auto(data['name_recipient'])
    if len(category_lst) != 1:
        await state.set_state(ParserAuto.category_state_auto)
        await message.answer(f'Введите категорию операции или выберете из списка ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_category_kbd()
                             )
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


@router.message(ParserAuto.recipient_state)
async def get_invalid_recipient_data(message: types.Message,):
    recipient_lst = await get_recipient_db()
    await message.answer(f'Введите корректного получателя платежа',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_recipient_kbd(recipient_lst))
