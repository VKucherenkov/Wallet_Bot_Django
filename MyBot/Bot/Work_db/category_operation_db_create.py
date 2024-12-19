import logging

from asgiref.sync import sync_to_async

from Bot.models import CategoryOperation, TypeOperation

logger = logging.getLogger(__name__)

type_category = {
    "Доход": ["ЗП", "Пенсия", "Соц. выплата", "Проценты банка"],
    "Расход": ["Продукты", 'Транспорт (ремонт)', 'ЖКХ', "Бензин", "Оплата кредита", "Одежда", "Электроника",
               "Бытовая техника", "Подарки", "Товары для детей", "Спортивные товары", "Табак"],
    "Перевод между своими счетами": ["Перевод"]
}

categoryes = {
    'Продукты': ['продукты', "кофе", "хлеб", "молоко", "сметана"],
    'Транспорт (ремонт)': ['транспорт (ремонт)', "запчасти"],
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


# @sync_to_async
def db_categoryoperation(msg=None):
    cat = [i for i in categoryes.keys()]
    cat_obj = CategoryOperation.objects.all()
    typeoperation = [(i, j) for i in cat for j, value in type_category.items() if i in value]
    db_name_all = [i.name_cat for i in cat_obj]
    logger.info(f'{db_name_all}')
    logger.info(f'{typeoperation}')
    if not db_name_all:
        for i, j in typeoperation:
            pk = TypeOperation.objects.get(name_type=j).pk
            CategoryOperation.objects.update_or_create(name_cat=f'{i}', TypeOperation_CategoryOperation_id=pk)
            logger.info(
                f'Категория операции: "{i}"\n'
                f'Тип операции: "{j}"\n'
                f'добавлен в базу данных {CategoryOperation.objects.get(name_cat=i).datetime_add}')
    else:
        logger.info(f'Таблица "Категория операции" уже была создана')
