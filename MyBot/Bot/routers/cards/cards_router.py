import logging

from aiogram import Router, F, types
from aiogram.enums import ParseMode

from Bot.Work_db.card_work import card_list
from Bot.keyboard.reply_keybord import my_card_kbd

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(F.text == 'Мои карты')
async def card_support(message: types.Message):
    """
    Обрабатывает команду "Мои карты" и отображает список карт пользователя.

    :param message: Объект сообщения.
    """
    # Логируем входящее сообщение
    logger.info(
        f'Пользователь: {message.chat.first_name} '
        f'с Telegram id: {message.from_user.id} написал:\n'
        f'{message.text}'
    )

    try:
        # Получаем список карт
        card_text, card_list_data = await card_list(message)
        logger.info(f"Результат выполнения card_list: {card_list_data}")

        if card_text:
            # Если карты есть, отправляем их пользователю
            await message.answer(
                f'Вот Ваши карты:\n\n{card_text}',
                parse_mode=ParseMode.HTML,
                reply_markup=my_card_kbd
            )
        else:
            # Если карт нет, отправляем сообщение об отсутствии карт
            await message.answer(
                'У Вас нет активных карт',
                reply_markup=my_card_kbd
            )

        # Предлагаем действия с картами
        await message.answer('Выберите, что надо сделать с картами')

    except Exception as err:
        # Логируем ошибку и уведомляем пользователя
        logger.error(f"Произошла ошибка при обработке команды 'Мои карты': {err}", exc_info=True)
        await message.answer(
            'Произошла ошибка при загрузке ваших карт. Пожалуйста, попробуйте позже.',
            reply_markup=my_card_kbd
        )
