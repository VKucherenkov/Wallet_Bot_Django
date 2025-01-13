from aiogram import Router, F, types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.load_db_operation import load_db_operaion
from Bot.keyboard.reply_keybord import start_kbd

router = Router(name=__name__)


@router.message(ParserAuto.resume_state, F.text=='Да')
async def get_balance(message: types.Message,
                        state: FSMContext):
    data = await state.update_data(telegram_id=message.from_user.id)
    await state.clear()
    await resume_input_notification(message=message, data=data)


async def resume_input_notification(message: types.Message, data):
    result = await load_db_operaion(data)
    if type(result) == int:
        text = '<code>Данные по операции записаны в базу данных.' + '\n' + f'ID операции:  {result}</code>'
    else:
        text = '<code>Данные по операции не записаны в базу данных. Внесите операцию вручную.' + '\n' + f'{result}</code>'
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=start_kbd)
    
@router.message(ParserAuto.resume_state, F.text=='Нет')
async def get_balance(message: types.Message,
                        state: FSMContext):
    await state.clear()
    text = '<code>Данные по операции не записаны в базу данных. Попоробуйте заново или внесите операцию вручную.</code>'
    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=start_kbd)
