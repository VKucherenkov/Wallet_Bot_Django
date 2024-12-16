from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои карты"),
            KeyboardButton(text="Мои финансы"),
            KeyboardButton(text="Ручной ввод операции")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует'
)

del_start_kbd = ReplyKeyboardRemove()

my_card_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить карту/кошелек"),
            KeyboardButton(text="Изменить данные по карте/кошельку"),
            KeyboardButton(text="Удалить карту/кошелек"),
            KeyboardButton(text="Главное меню"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите интересующий Вас пункт меню "Работа с картами/кошельками"'
)

del_my_card_kbd = ReplyKeyboardRemove()

add_card_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Назад"),
            KeyboardButton(text='Отмена (выход к меню "Работа с картами/кошельками")'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Введите запрашиваему информацию, либо выберете пункт меню ниже'
)

del_add_card_kbd = ReplyKeyboardRemove()
