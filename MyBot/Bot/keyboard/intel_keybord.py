import telebot

intel_marcup = telebot.types.InlineKeyboardMarkup()
button_add = telebot.types.InlineKeyboardButton(text="Добавить карту",
                                                 callback_data='add_card')
button_change = telebot.types.InlineKeyboardButton(text="Изменить карту",
                                                 callback_data='change_card')
button_delete = telebot.types.InlineKeyboardButton(text="Удалить карту",
                                                 callback_data='delete_card')
intel_marcup.add(button_add, button_change, button_delete)

if __name__ == '__main__':
    main()
