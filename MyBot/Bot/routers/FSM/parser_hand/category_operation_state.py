from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.card_work import card_list_for_kb

from Bot.keyboard.reply_keybord import start_kbd, get_card_kbd, get_category_kbd
from Bot.validators.valid_categoryes import validator_categoryes

router = Router(name=__name__)


@router.message(ParserHand.category_state, F.text, F.func(validator_categoryes))
async def get_name_category(message: types.Message,
                            state: FSMContext):
    await state.update_data(name_cat=message.text.lower())
    if message.text.lower() == 'перевод':
        await state.set_state(ParserHand.card_number_state_out)
        card_list = await card_list_for_kb(message)
        await message.answer(f'Введите номер новой карты с которой'
                             f'списываются денежные средства, или выберите из предложенных ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_card_kbd(card_list))
    else:
        await state.set_state(ParserHand.card_number_state)
        card_list = await card_list_for_kb(message)
        await message.answer(f'Введите номер новой карты, или выберите из предложенных ниже',
                             parse_mode=ParseMode.HTML,
                             reply_markup=get_card_kbd(card_list))



@router.message(ParserHand.category_state)
async def get_invalid_name_category(message: types.Message, ):
    await message.answer(f'Введите корректную категорию операции',
                         parse_mode=ParseMode.HTML,
                         reply_markup=get_category_kbd())
