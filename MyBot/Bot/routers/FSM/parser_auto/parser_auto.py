import logging
from decimal import Decimal

from aiogram import types, Router
from aiogram.enums import ParseMode

from aiogram.fsm.context import FSMContext
from django.conf import settings
from aiogram import F

from Bot.FSM_processing.states import ParserAuto
from Bot.Parser_notification.logik_parser_sms import parser_logic_notification
from Bot.Work_db.card_work import card_list, card_number
from Bot.Work_db.category_operation_db import get_name_category_auto, get_categories_for_keyboard
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.Work_db.type_operation_db import get_type_for_keyboard
from Bot.keyboard.reply_keybord import start_kbd, get_prev_cancel_kbd, get_recipient_kbd, get_category_kbd, \
    get_yes_no_kbd, get_type_kbd


logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.text == 'Ввод типичной операции')
async def start_auto_parser(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду "Ввод типичной операции" и устанавливает начальное состояние.

    :param message: Объект сообщения.
    :param state: Состояние FSMContext.
    """
    try:
        # Устанавливаем начальное состояние
        await state.set_state(ParserAuto.start_state)

        # Логируем входящее сообщение
        logger.info(
            f'Пользователь: {message.chat.first_name} '
            f'с Telegram id: {message.from_user.id} написал:\n'
            f'{message.text}'
        )

        # Отправляем инструкцию пользователю
        text_message = 'В поле ввода текста вставьте уведомление, полученное из банка'
        await message.answer(text=text_message, parse_mode=ParseMode.HTML, reply_markup=start_kbd)

        # Уведомляем администратора, если пользователь не является им
        if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
            admin_message = (
                f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n'
                f'<code>{message.date}\n ------------- \n{message.text}</code>'
            )
            await message.bot.send_message(
                chat_id=settings.TELEGRAM_ID_ADMIN,
                text=admin_message,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Администратор уведомлен о действии пользователя {message.from_user.id}.")

    except Exception as err:
        # Логируем ошибку
        logger.error(f"Произошла ошибка при обработке команды 'Ввод типичной операции': {err}", exc_info=True)
        await message.answer(
            text='<code>Произошла ошибка при обработке вашего запроса. Попробуйте позже.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )


@router.message(ParserAuto.start_state, F.text.lower().contains('['))
async def recipient_auto_parser(message: types.Message, state: FSMContext):
    try:
        # Парсинг сообщения
        data, data_txt = await parser_logic_notification(message)
        await clean_data(data)  # Очистка и форматирование данных

        # Уведомление администратора, если необходимо
        if message.from_user.id != settings.TELEGRAM_ID_ADMIN:
            await notify_admin(message)

        # Обновление состояния с распарсенными данными
        await update_state(state, data)

        # Ответ пользователю
        await message.answer(data_txt, parse_mode=ParseMode.HTML)
        await message.answer("принят", parse_mode=ParseMode.HTML, reply_markup=start_kbd)

        # Проверка на отсутствие данных и запрос у пользователя
        await handle_missing_data(message, state, data)

    except Exception as e:
        logger.error(f"Ошибка в recipient_auto_parser: {e}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте еще раз.")

async def clean_data(data):
    data['amount_operation'] = data['amount_operation'].replace(',', '.').replace(' ', '').replace('[NBSP]', '')
    data['balans'] = data['balans'].replace(',', '.').replace(' ', '').replace('[NBSP]', '')

async def notify_admin(message):
    await message.bot.send_message(
        chat_id=settings.TELEGRAM_ID_ADMIN,
        text=f'Пользователь с ID: <b>{message.from_user.id}</b>, написал:\n<code>{message.date}\n ------------- \n{message.text}</code>',
        parse_mode=ParseMode.HTML
    )

async def update_state(state, data):
    await state.update_data(
        number_card=data['number_card'],
        name_card=data['name_card'],
        name_bank=data['name_bank'],
        balans=Decimal(data['balans']),
        amount_operation=Decimal(data['amount_operation']),
        name_recipient=data['name_recipient'],
        recipient_in_notification=data['recipient_in_notification'],
        name_cat=data['name_cat'],
        name_type=data['name_type'],
        datetime_amount=data['datetime_amount'],
        note_operation=data['note_operation']
    )

async def handle_missing_data(message, state, data):
    card_num = await card_number(data['number_card'])
    recipient_lst = await get_recipient_db(data['name_recipient'])
    category_lst = await get_name_category_auto(data['name_recipient'])

    if not card_num:
        await state.set_state(ParserAuto.card_name_state)
        await message.answer("Введите имя карты", parse_mode=ParseMode.HTML, reply_markup=get_prev_cancel_kbd())
    elif data['name_recipient'].capitalize() not in recipient_lst:
        recipient_lst += [data['name_recipient'].capitalize()]
        await state.set_state(ParserAuto.recipient_state)
        await message.answer(
            "Введите получателя платежа или выберите из списка ниже",
            parse_mode=ParseMode.HTML,
            reply_markup=get_recipient_kbd(recipient_lst)
        )
    elif not data['name_type']:
        types = await get_type_for_keyboard()
        await state.set_state(ParserAuto.type_state_auto)
        await message.answer(
            "Введите тип операции или выберите из списка ниже",
            parse_mode=ParseMode.HTML,
            reply_markup=get_type_kbd(types)
        )
    elif len(category_lst) != 1:
        categories_lst = await get_categories_for_keyboard()
        await state.set_state(ParserAuto.category_state_auto)
        await message.answer(
            "Введите категорию операции или выберите из списка ниже",
            parse_mode=ParseMode.HTML,
            reply_markup=get_category_kbd(categories_lst)
        )
    else:
        await state.update_data(name_cat=category_lst[0])
        await display_summary(message, state)

async def display_summary(message, state):
    data = await state.get_data()
    text = ''.join(f'<code>{key:<17} ------ {value}</code>\n' for key, value in data.items())
    await state.set_state(ParserAuto.resume_state)
    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await message.answer(
        "Проверьте и подтвердите правильность введённых данных по операции",
        parse_mode=ParseMode.HTML,
        reply_markup=get_yes_no_kbd()
    )