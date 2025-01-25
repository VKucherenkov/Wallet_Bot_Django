from aiogram import Router

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.load_db_operation import load_db_operation
from Bot.keyboard.reply_keybord import start_kbd

from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import logging

router = Router(name=__name__)

logger = logging.getLogger(__name__)

@router.message(ParserAuto.resume_state, F.text == 'Да')
async def get_balance_yes(message: types.Message, state: FSMContext):
    """
    Обрабатывает ответ "Да" и сохраняет данные операции в базу данных.
    """
    try:
        # Обновляем данные в состоянии
        data = await state.update_data(telegram_id=message.from_user.id)
        await state.clear()

        # Сохраняем данные в базу и получаем результат
        result, text = await load_db_operation(data)

        # Формируем сообщение для пользователя
        if isinstance(result, int):
            response_text = (
                f'<code>Данные по операции записаны в базу данных.\n'
                f'ID операции: {result}</code>'
            )
        else:
            response_text = (
                f'<code>Данные по операции не записаны в базу данных. '
                f'Внесите операцию вручную.\n{result}</code>'
            )

        # Логируем результат
        logger.info(f"Пользователь {message.from_user.id} подтвердил запись операции. Результат: {result}")

        # Отправляем сообщение пользователю
        await message.answer(text=response_text, parse_mode=ParseMode.HTML, reply_markup=start_kbd)

    except Exception as err:
        # Логируем ошибку
        logger.error(f"Произошла ошибка при обработке ответа 'Да': {err}", exc_info=True)
        await message.answer(
            text='<code>Произошла ошибка при обработке вашего запроса. Попробуйте позже.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )

@router.message(ParserAuto.resume_state, F.text == 'Нет')
async def get_balance_no(message: types.Message, state: FSMContext):
    """
    Обрабатывает ответ "Нет" и сообщает пользователю, что данные не были записаны.
    """
    try:
        # Очищаем состояние
        await state.clear()

        # Логируем действие
        logger.info(f"Пользователь {message.from_user.id} отказался от записи операции.")

        # Отправляем сообщение пользователю
        await message.answer(
            text='<code>Данные по операции не записаны в базу данных. Попробуйте заново или внесите операцию вручную.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )

    except Exception as err:
        # Логируем ошибку
        logger.error(f"Произошла ошибка при обработке ответа 'Нет': {err}", exc_info=True)
        await message.answer(
            text='<code>Произошла ошибка при обработке вашего запроса. Попробуйте позже.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )