from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.keyboard.reply_keybord import get_category_kbd, choice_type_kbd
from Bot.validators.validator_type import validate_type

router = Router(name=__name__)


@router.message(ParserHand.type_state,
                F.text, F.func(validate_type))
async def get_name_type(message: types.Message,
                        state: FSMContext):
    await state.update_data(name_type=message.text.lower())
    await state.set_state(ParserHand.category_state)
    await message.answer(f'Введите категорию операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_category_kbd())


@router.message(ParserHand.type_state)
async def get_invalid_name_type(message: types.Message, ):
    await message.answer(f'Введите корректный тип операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=choice_type_kbd)
