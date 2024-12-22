banks = {
    "Сбербанк": ["сбер", "сбербанк"],
    "Яндекс банк": ["яндекс", "яндексбанк", "яндекс банк"],
    "Альфа банк": ["альфа", "альфабанк", "альфа банк"],
    "Совкомбанк": ["совкомбанк", "совком банк", "совком"],
    "МТС банк": ["мтс", "мтсбанк", "мтс банк"],
    "Тинькофф банк": ["тинькофф", "тинькоф", "тинькоффбанк", "тинькофбанк", "тинькофф банк", "тинькоф банк"],
    "ВТБ": ["втб", "втб банк", "втббанк"],
}

type_category = {
    "Доход": ["ЗП", "Пенсия", "Соц. выплата", "Проценты банка", 'зачисление', 'поступление', ],
    "Расход": ["Продукты", 'Транспорт (ремонт)', 'ЖКХ', "Бензин", "Оплата кредита", "Одежда", "Электроника",
               "Бытовая техника", "Подарки", "Товары для детей", "Спортивные товары", "Табак"],
    "Перевод между своими счетами": ["Перевод"]
}

categoryes = {
    'Продукты': ['продукты', "кофе", "хлеб", "молоко", "сметана"],
    'Транспорт (ремонт)': ['транспорт (ремонт)', "запчасти", 'мост', "понтонник", "пантон", "понтон"],
    'ЖКХ': ['ЖКХ', "свет", "тепло", "энергия", "электричество", "коммуналка", "газ"],
    "Бензин": ["бензин", "топливо", "АЗС", "заправка"],
    "ЗП": ["ЗП", "зарплата", "аванс", "получка", ],
    "Пенсия": ["пенс"],
    "Соц. выплата": ["соц. выплата", "соцвыплата"],
    "Проценты банка": ["проценты банка", "процент"],
    "Оплата кредита": ["оплата кредита", "кредит"],
    "Перевод": ["перевод"],
    "Одежда": ["Одежда"],
    "Электроника": ["Электроника"],
    "Бытовая техника": ["Бытовая техника"],
    "Подарки": ["Подарки"],
    "Товары для детей": ["Товары для детей"],
    "Спортивные товары": ["Спортивные товары"],
    "Табак": ["Табак"],
}

data_parser = {
    'name_bank': '',
    'name_card': '',
    'name_type': '',
    'name_cat': '',
    'datetime_amount': '',
    'amount_operation': '',
    'note_operation': '',
    'name_recipient': '',
    'recipient_in_notification': '',
    'balans': '',
    'number_card':''
}