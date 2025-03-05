import logging

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from Bot.Work_db.category_operation_db import get_categories_for_keyboard
from Bot.common.global_variable import type_category, categoryes, banks, card_type

logger = logging.getLogger(name=__name__)


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


def get_prev_cancel_builder():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Назад")
    builder.button(text="Отмена")
    return builder


def get_prev_cancel_kbd():
    builder = ReplyKeyboardBuilder()
    builder.attach(get_prev_cancel_builder())
    return builder.as_markup(resize_keyboard=True)


def get_currency_kbd():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Доллар")
    builder.button(text="Рубль")
    return builder.as_markup(resize_keyboard=True)


def get_type_kbd(types):
    builder = ReplyKeyboardBuilder()
    for button in sorted(types):
        builder.button(text=button)
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_category_kbd(categories):
    builder = ReplyKeyboardBuilder()
    for button in sorted(categories):
        builder.button(text=button)
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
            KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_bank_kbd():
    builder = ReplyKeyboardBuilder()
    for button in banks.keys():
        builder.button(text=button)
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_card_kbd(card_list):
    builder = ReplyKeyboardBuilder()
    for button in card_list:
        builder.button(text=f'{button["Номер"]}')
    if not card_list:
        builder.button(text=f'Сохраненные карты отсутствуют')
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_card_type_kbd():
    builder = ReplyKeyboardBuilder()
    for type in card_type.values():
        builder.button(text=type)
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_recipient_kbd(recipient_lst):
    builder = ReplyKeyboardBuilder()
    for button in recipient_lst:
        builder.button(text=button)
    builder.adjust(3)
    builder.row(KeyboardButton(text='Назад'),
                KeyboardButton(text='Отмена'))
    return builder.as_markup(resize_keyboard=True)


def get_yes_no_kbd():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Да')
    builder.button(text='Нет')
    return builder.as_markup(resize_keyboard=True)
