import logging

from aiogram import Router, F, types

from Bot.FSM_processing.states import ParserHand
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.Parser_notification.logik_parser_sms import get_datetime
from Bot.keyboard.reply_keybord import get_prev_cancel_kbd, choice_type_kbd
from Bot.validators.validator_date_amount import validator_date_amount

router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message(ParserHand.date_amount_state, F.text, F.func(validator_date_amount))
async def get_number_card(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод даты и времени операции, проверяет ее и переходит к следующему шагу.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        datetime_amount = get_datetime(message.text)  # Сохраняем дату в переменной
        await state.update_data(datetime_amount=datetime_amount)
        await state.set_state(ParserHand.type_state)
        await message.answer(f'Введите тип операции',
                             parse_mode=ParseMode.HTML,
                             reply_markup=choice_type_kbd)
    except Exception as e:
        logger.error(f"Ошибка при обработке даты операции: {e}")
        await message.answer(
            "Произошла ошибка при обработке даты операции. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.date_amount_state)
async def get_invalid_number_card(message: types.Message):
    """
    Обрабатывает ввод некорректного ввода даты операции и предлагает ввести верную дату.

    :param message: Объект сообщения от пользователя.
    """

    # Отправляем сообщение с клавиатурой
    await message.answer(
        f"Введите корректную дату операции в формате 'день, месяц, год, час, минуты'. "
        f"Например для даты 1 января 2025 года 9:05 часов, следует ввести: 1, 1, 2025, 9, 5.",
        parse_mode=ParseMode.HTML,
        reply_markup=get_prev_cancel_kbd
    )
