from asgiref.sync import sync_to_async

from Bot.models import TypeOperation, CategoryOperation, Recipient, BankCard, CardUser, OperationUser, TelegramUser


@sync_to_async
def load_db_operaion(data):
    try:
        [print(key, value, sep='\n') for key, value in data.items()]
        types = [i.name_type.lower() for i in TypeOperation.objects.all()]
        if data['name_type'].lower() not in types:
            TypeOperation.objects.create(name_type=data['name_type'])
        types_id = TypeOperation.objects.get(name_type=data['name_type']).id
        print("Тип операций записан в базу")

        category = [i.name_cat.lower() for i in CategoryOperation.objects.all()]
        if data['name_cat'].lower() not in category:
            CategoryOperation.objects.create(name_cat=data['name_cat'],
                                             TypeOperation_CategoryOperation_id=types_id)
        category_id = CategoryOperation.objects.get(name_cat=data['name_cat']).id
        print("Категория операции записана в базу")


        recipient = [i.name_recipient.lower() for i in Recipient.objects.all()]
        if not recipient or data['name_recipient'].lower() not in recipient:
            Recipient.objects.create(name_recipient=data['name_recipient'],
                                     Recipient_CategoryOperation_id=category_id)
        print("Реципиент записан в базу")

        banks = [i.name_bank for i in BankCard.objects.all()]
        if all([data['name_bank'].lower() not in i.lower() for i in banks]):
            BankCard.objects.create(name_bank=data['name_bank'].lower())
        bank_id = BankCard.objects.get(name_bank=data['name_bank'].lower()).id
        print("Имя банка записано в базу")

        cards = [i.number_card for i in CardUser.objects.all()]
        user_id = TelegramUser.objects.get(telegram_id=data['telegram_id']).id
        if not cards or data['number_card'] not in cards:
            CardUser.objects.create(number_card=data['number_card'],
                                    name_card=data['name_card'].lower(),
                                    BankCard_CardUser_id=bank_id,
                                    TelegramUser_CardUser_id=user_id)
        card_id = CardUser.objects.get(number_card=data['number_card']).id
        print("Имя и номер карты записаны в базу")


        OperationUser.objects.create(datetime_amount=data['datetime_amount'],
                                     amount_operation=data['amount_operation'],
                                     CardUser_OperationUser_id=card_id,
                                     CategoryOperation_OperationUser_id=category_id)
        operation_id = CardUser.objects.get(datetime_amount=data['datetime_amount']).id
        print("Операция записана в базу")

    except Exception as err:
        print(err)
        return False
    return operation_id
