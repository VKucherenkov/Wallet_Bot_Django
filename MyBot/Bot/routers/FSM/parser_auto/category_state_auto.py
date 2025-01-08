from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.card_work import card_list_for_kb
from Bot.keyboard.reply_keybord import get_card_kbd, get_category_kbd, get_yes_no_kbd
from Bot.validators import validator_categoryes


router = Router(name=__name__)

@router.message(ParserAuto.category_state_auto, F.text)
async def get_name_category(message: types.Message,
                            state: FSMContext):
    data = await state.update_data(name_cat=message.text.lower())
    text = ''
    for key, value in data.items():
        text += f'<code>{key:<17} ------ {value}</code>\n'
    await state.set_state(ParserAuto.resume_state)
    await message.answer(text=text,
                         parse_mode=ParseMode.HTML)
    await message.answer(f'Проверьте и подтвердите правильность введенных данных по операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_yes_no_kbd())


@router.message(ParserAuto.category_state_auto)
async def get_invalid_name_category(message: types.Message, ):
    await message.answer(f'Введите корректную категорию операции, или выберите из предложенных ниже',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_category_kbd())
