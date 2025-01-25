import logging

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from Bot.FSM_processing.states import ParserAuto
from Bot.Work_db.category_operation_db import get_name_category_auto, get_categories_for_keyboard
from Bot.Work_db.recipient_db import get_recipient_db
from Bot.Work_db.type_operation_db import get_type_for_keyboard
from Bot.keyboard.reply_keybord import get_recipient_kbd, get_category_kbd, get_yes_no_kbd, get_type_kbd, start_kbd

router = Router(name=__name__)



logger = logging.getLogger(__name__)


@router.message(ParserAuto.recipient_state, F.text)
async def get_recipient_data(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод данных о получателе платежа.
    """
    try:
        # Обновляем данные в состоянии
        data = await state.update_data(name_recipient=message.text.lower())

        # Получаем категории для получателя
        category_lst = await get_name_category_auto(data['name_recipient'])
        categories_lst = await get_categories_for_keyboard()

        if not data.get('name_type'):
            # Если тип операции не указан, запрашиваем его
            types = await get_type_for_keyboard()
            await state.set_state(ParserAuto.type_state_auto)
            await message.answer(
                'Введите тип операции или выберите из списка ниже',
                parse_mode=ParseMode.HTML,
                reply_markup=get_type_kbd(types)
            )
            logger.info(
                f"Пользователь {message.from_user.id} ввел получателя: {data['name_recipient']}. Запрошен тип операции.")
        elif not category_lst or len(category_lst) != 1:
            # Если категория не указана или их несколько, запрашиваем категорию
            await state.set_state(ParserAuto.category_state_auto)
            await message.answer(
                'Введите категорию операции или выберите из списка ниже',
                parse_mode=ParseMode.HTML,
                reply_markup=get_category_kbd(categories_lst)
            )
            logger.info(
                f"Пользователь {message.from_user.id} ввел получателя: {data['name_recipient']}. Запрошена категория операции.")
        else:
            # Если категория одна, переходим к подтверждению данных
            data = await state.update_data(name_cat=category_lst[0])
            text = '\n'.join(f'<code>{key:<17} ------ {value}</code>' for key, value in data.items())
            await state.set_state(ParserAuto.resume_state)
            await message.answer(
                text=text,
                parse_mode=ParseMode.HTML
            )
            await message.answer(
                'Проверьте и подтвердите правильность введенных данных по операции',
                parse_mode=ParseMode.HTML,
                reply_markup=get_yes_no_kbd()
            )
            logger.info(
                f"Пользователь {message.from_user.id} ввел получателя: {data['name_recipient']}. Данные готовы к подтверждению.")

    except Exception as err:
        # Логируем ошибку
        logger.error(f"Произошла ошибка при обработке получателя: {err}", exc_info=True)
        await message.answer(
            text='<code>Произошла ошибка при обработке вашего запроса. Попробуйте позже.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )


@router.message(ParserAuto.recipient_state)
async def get_invalid_recipient_data(message: types.Message):
    """
    Обрабатывает некорректный ввод получателя.
    """
    try:
        # Получаем список получателей
        recipient_lst = await get_recipient_db()

        # Логируем действие
        logger.info(f"Пользователь {message.from_user.id} ввел некорректного получателя.")

        # Отправляем сообщение с предложением выбрать получателя
        await message.answer(
            'Введите корректного получателя платежа',
            parse_mode=ParseMode.HTML,
            reply_markup=get_recipient_kbd(recipient_lst)
        )

    except Exception as err:
        # Логируем ошибку
        logger.error(f"Произошла ошибка при обработке некорректного получателя: {err}", exc_info=True)
        await message.answer(
            text='<code>Произошла ошибка при обработке вашего запроса. Попробуйте позже.</code>',
            parse_mode=ParseMode.HTML,
            reply_markup=start_kbd
        )

# @router.message(ParserAuto.recipient_state, F.text)
# async def get_recipient_data(message: types.Message, state: FSMContext):
#     data = await state.update_data(name_recipient=message.text.lower())
#     category_lst = await get_name_category_auto(data['name_recipient'])
#     categories_lst = await get_categories_for_keyboard()
#     if not data['name_type']:
#         types = await get_type_for_keyboard()
#         await state.set_state(ParserAuto.type_state_auto)
#         await message.answer(f'Введите тип операции или выберете из списка ниже',
#                              parse_mode=ParseMode.HTML,
#                              reply_markup=get_type_kbd(types))
#     elif not category_lst or len(category_lst) != 1:
#         await state.set_state(ParserAuto.category_state_auto)
#         await message.answer(f'Введите категорию операции или выберете из списка ниже',
#                              parse_mode=ParseMode.HTML,
#                              reply_markup=get_category_kbd(categories_lst)
#                              )
#     else:
#         data = await state.update_data(name_cat=category_lst[0])
#         text = ''
#         for key, value in data.items():
#             text += f'<code>{key:<17} ------ {value}</code>\n'
#         await state.set_state(ParserAuto.resume_state)
#         await message.answer(text=text,
#                              parse_mode=ParseMode.HTML)
#         await message.answer(f'Проверьте и подтвердите правильность введенных данных по операции',
#                              parse_mode=ParseMode.HTML,
#                              reply_markup=get_yes_no_kbd())
#
#
# @router.message(ParserAuto.recipient_state)
# async def get_invalid_recipient_data(message: types.Message,):
#     recipient_lst = await get_recipient_db()
#     await message.answer(f'Введите корректного получателя платежа',
#                          parse_mode=ParseMode.HTML,
#                          reply_markup=get_recipient_kbd(recipient_lst))
