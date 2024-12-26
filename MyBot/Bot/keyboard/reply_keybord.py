from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from Bot.common.global_variable import type_category, categoryes, banks

start_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Мои карты"),
            KeyboardButton(text="Мои финансы"),
        ],
        [
            KeyboardButton(text="Ввод типичной операции"),
            KeyboardButton(text="Ручной ввод операции")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите что Вас интересует'
)

del_start_kbd = ReplyKeyboardRemove()

my_card_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить карту"),
            KeyboardButton(text="Изменить карту"),
            KeyboardButton(text="Удалить карту"),
        ],
        [
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


choice_type_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=type_str) for type_str in type_category.keys()
        ],
        [
            KeyboardButton(text='Добавить тип операции'),
            KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена'),
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Выберите тип операции'
)


def get_category_kbd() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button in categoryes.keys():
        builder.button(text=button)
    builder.button(text="Назад")
    builder.button(text="Отмена")
    builder.adjust(7)
    return builder.as_markup(resize_keyboard=True)


def get_bank_kbd() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for button in banks.keys():
        builder.button(text=button)
    builder.button(text="Назад")
    builder.button(text="Отмена")
    builder.adjust(7)
    return builder.as_markup(resize_keyboard=True)