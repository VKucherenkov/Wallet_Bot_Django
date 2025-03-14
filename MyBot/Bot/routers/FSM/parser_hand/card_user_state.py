import logging

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from Bot.FSM_processing.states import ParserHand
from Bot.Work_db.bank_db import get_bank_name_by_card
from Bot.Work_db.card_work import card_number, card_name, card_list_for_kb, get_credit_limit_card, get_type_card, \
    get_currency_card
from Bot.keyboard.reply_keybord import get_bank_kbd, get_prev_cancel_kbd, get_card_kbd, get_card_type_kbd, \
    get_currency_kbd
from Bot.validators.valid_card_name import validator_name_card, validator_type_card, validator_limit_card, \
    validator_currency_card
from Bot.validators.valid_card_number import validator_card_number


router = Router(name=__name__)

logger = logging.getLogger(__name__)


@router.message(ParserHand.card_number_state_out, F.text, F.func(validator_card_number))
async def get_number_card(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод номера карты, проверяет его и переходит к следующему шагу.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    cardnumber = message.text  # Сохраняем номер карты в переменной
    await state.update_data(number_card_out=cardnumber)

    try:
        # Проверяем, существует ли карта
        if await card_number(cardnumber):
            # Получаем данные карты
            name_card_out = await card_name(cardnumber)
            name_bank_out = await get_bank_name_by_card(cardnumber)
            type_card_out = await get_type_card(cardnumber)
            currency_card_out = await get_currency_card(cardnumber)
            credit_limit_out = await get_credit_limit_card(cardnumber)

            # Обновляем состояние
            await state.update_data(name_card_out=name_card_out, name_bank_out=name_bank_out, type_card_out=type_card_out, currency_card_out=currency_card_out, credit_limit_out=credit_limit_out)
            await state.set_state(ParserHand.operation_state_out)

            # Запрашиваем сумму операции
            await message.answer(
                "Введите сумму по операции",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
        else:
            # Если карта не найдена, запрашиваем имя карты
            await state.set_state(ParserHand.card_name_state_out)
            await message.answer(
                "Введите имя карты",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке номера карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_number_state, F.text, F.func(validator_card_number))
async def get_number_card(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод номера карты, проверяет его и переходит к следующему шагу.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    cardnumber = message.text  # Сохраняем номер карты в переменной
    await state.update_data(number_card=cardnumber)

    try:
        # Проверяем, существует ли карта
        if await card_number(cardnumber):
            # Получаем данные карты
            name_card = await card_name(cardnumber)
            name_bank = await get_bank_name_by_card(cardnumber)
            type_card = await get_type_card(cardnumber)
            currency_card = await get_currency_card(cardnumber)
            credit_limit = await get_credit_limit_card(cardnumber)

            # Обновляем состояние
            await state.update_data(name_card=name_card, name_bank=name_bank, currency_card=currency_card, type_card=type_card, credit_limit=credit_limit)
            await state.set_state(ParserHand.operation_state)

            # Запрашиваем сумму операции
            await message.answer(
                "Введите сумму по операции",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
        else:
            # Если карта не найдена, запрашиваем имя карты
            await state.set_state(ParserHand.card_name_state)
            await message.answer(
                "Введите имя карты",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке номера карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_number_state_out)
@router.message(ParserHand.card_number_state)
async def get_invalid_number_card(message: types.Message):
    """
    Обрабатывает ввод некорректного номера карты и предлагает выбрать карту из списка.

    :param message: Объект сообщения от пользователя.
    """
    try:
        # Получаем список карт для клавиатуры
        card_list = await card_list_for_kb(message)

        # Отправляем сообщение с клавиатурой
        await message.answer(
            "Введите корректный номер карты или выберите карту из списка:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_card_kbd(card_list)
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке некорректного номера карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML
        )


@router.message(ParserHand.card_name_state_out, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод названия карты и переходит к запросу валюты карты.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем название карты в состоянии
        card_name_out = message.text.lower()
        await state.update_data(name_card_out=card_name_out)

        # Переходим к следующему шагу — запросу валюты карты
        await state.set_state(ParserHand.card_currency_state_out)
        await message.answer(
            "Введите валюту карты:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке названия карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_name_state, F.text, F.func(validator_name_card))
async def get_name_card(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод названия карты и переходит к запросу валюты карты.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем название карты в состоянии
        card_name = message.text.lower()
        await state.update_data(name_card=card_name)

        # Переходим к следующему шагу — запросу валюты карты
        await state.set_state(ParserHand.card_currency_state)
        await message.answer(
            "Введите валюту карты:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке названия карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_name_state_out)
@router.message(ParserHand.card_name_state)
async def get_invalid_name_card(message: types.Message):
    """
    Обрабатывает ввод некорректного названия карты и просит пользователя ввести корректное имя.

    :param message: Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с просьбой ввести корректное имя карты
        await message.answer(
            "Введите корректное имя карты. Пример: 'мир'.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке некорректного названия карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_currency_state_out, F.text, F.func(validator_currency_card))
async def get_currency_card_out_input(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод валюты карты и переходит к запросу типа карты.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем валюту карты в состоянии
        card_currency_out = message.text.lower()
        await state.update_data(currency_card_out=card_currency_out)

        # Переходим к следующему шагу — запросу типа карты
        await state.set_state(ParserHand.card_type_state_out)
        await message.answer(
            "Введите тип карты:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_card_type_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке валюты карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )


@router.message(ParserHand.card_currency_state, F.text, F.func(validator_currency_card))
async def get_currency_card_input(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод валюты карты и переходит к запросу типа карты.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем валюту карты в состоянии
        card_currency = message.text.lower()
        await state.update_data(currency_card=card_currency)

        # Переходим к следующему шагу — запросу типа карты
        await state.set_state(ParserHand.card_type_state)
        await message.answer(
            "Введите тип карты:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_card_type_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке валюты карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )


@router.message(ParserHand.card_currency_state_out)
@router.message(ParserHand.card_currency_state)
async def get_invalid_currency_card(message: types.Message):
    """
    Обрабатывает ввод некорректной валюты карты и просит пользователя ввести корректную валюту.

    :param message: Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с просьбой ввести корректную валюту карты
        await message.answer(
            "Введите корректную валюту карты. Пример: 'USD'.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке некорректной валюты карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_currency_kbd()
        )


@router.message(ParserHand.card_type_state_out, F.text, F.func(validator_type_card))
async def get_type_card_hand(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод типа карты и переходит к запросу кредитного лимита, если карта кредитная.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем тип карты в состоянии
        type_card_out = message.text.lower()
        await state.update_data(type_card_out=type_card_out)

        # Переходим к следующему шагу — запросу наименования банка
        if type_card_out == 'кредитная':
            await state.set_state(ParserHand.card_credit_state_out)
            await message.answer(
                "Введите кредитный лимит по карте, установленный банком:",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
        else:
            await state.update_data(credit_limit=0)
            await state.set_state(ParserHand.bank_state_out)
            await message.answer(
                "Введите наименование банка или выберите из списка:",
                parse_mode=ParseMode.HTML,
                reply_markup=get_bank_kbd()
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке типа карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_bank_kbd()
        )


@router.message(ParserHand.card_type_state, F.text, F.func(validator_type_card))
async def get_type_card_hand(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод типа карты и переходит к запросу кредитного лимита, если карта кредитная.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем тип карты в состоянии
        type_card = message.text.lower()
        await state.update_data(type_card=type_card)

        # Переходим к следующему шагу — запросу наименования банка
        if type_card == 'кредитная':
            await state.set_state(ParserHand.card_credit_state)
            await message.answer(
                "Введите кредитный лимит по карте, установленный банком:",
                parse_mode=ParseMode.HTML,
                reply_markup=get_prev_cancel_kbd()
            )
        else:
            await state.update_data(credit_limit=0)
            await state.set_state(ParserHand.bank_state)
            await message.answer(
                "Введите наименование банка или выберите из списка:",
                parse_mode=ParseMode.HTML,
                reply_markup=get_bank_kbd()
            )
    except Exception as e:
        logger.error(f"Ошибка при обработке типа карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_bank_kbd()
        )


@router.message(ParserHand.card_type_state_out)
@router.message(ParserHand.card_type_state)
async def get_invalid_name_card(message: types.Message):
    """
    Обрабатывает ввод некорректного типа карты и просит пользователя ввести корректный тип.

    :param message: Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с просьбой ввести корректный тип карты
        await message.answer(
            "Введите корректный тип карты. Пример: 'кредитная', 'дебетовая'.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_card_type_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке некорректного типа карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_credit_state_out, F.text, F.func(validator_limit_card))
async def get_type_card_hand(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод кредитного лимита карты и переходит к запросу наименование банка.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем тип карты в состоянии
        credit_limit_out = message.text.lower()
        await state.update_data(credit_limit_out=credit_limit_out)

        # Переходим к следующему шагу — запросу наименования банка
        await state.set_state(ParserHand.bank_state_out)
        await message.answer(
            "Введите наименование банка или выберите из списка:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_bank_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке кредитного лимита карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_credit_state, F.text, F.func(validator_limit_card))
async def get_type_card_hand(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод кредитного лимита карты и переходит к запросу наименование банка.

    :param message: Объект сообщения от пользователя.
    :param state: Контекст состояния FSM.
    """
    try:
        # Сохраняем тип карты в состоянии
        credit_limit = message.text.lower()
        await state.update_data(credit_limit=credit_limit)

        # Переходим к следующему шагу — запросу наименования банка
        await state.set_state(ParserHand.bank_state)
        await message.answer(
            "Введите наименование банка или выберите из списка:",
            parse_mode=ParseMode.HTML,
            reply_markup=get_bank_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке кредитного лимита карты: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )


@router.message(ParserHand.card_credit_state_out)
@router.message(ParserHand.card_credit_state)
async def get_invalid_name_card(message: types.Message):
    """
    Обрабатывает ввод некорректного кредитного лимита по карте и просит пользователя ввести корректный лимит.

    :param message: Объект сообщения от пользователя.
    """
    try:
        # Отправляем сообщение с просьбой ввести корректный тип карты
        await message.answer(
            "Введите корректный кредитного лимита по карте. Кредитный лимит должен быть положительным числом",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )
    except Exception as e:
        logger.error(f"Ошибка при обработке некорректного кредитного лимита по карте: {e}")
        await message.answer(
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            parse_mode=ParseMode.HTML,
            reply_markup=get_prev_cancel_kbd()
        )