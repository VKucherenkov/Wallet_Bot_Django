from asgiref.sync import sync_to_async

from Bot.models import TypeOperation, CategoryOperation, Recipient, BankCard, CardUser, OperationUser, TelegramUser


@sync_to_async
def load_db_operaion(data):
    try:
        [print(f'{key:<15} --- {value:<20}\n') for key, value in data.items()]
        types = [i.name_type.lower() for i in TypeOperation.objects.all()]
        if data['name_type'].lower() not in types:
            TypeOperation.objects.create(name_type=data['name_type'].lower())
        types_id = TypeOperation.objects.get(name_type=data['name_type']).id
        print("Тип операций записан в базу")

        category = [i.name_cat.lower() for i in CategoryOperation.objects.all()]
        if data['name_cat'].lower() not in category:
            CategoryOperation.objects.create(name_cat=data['name_cat'].lower(),
                                             TypeOperation_CategoryOperation_id=types_id)
        category_id = CategoryOperation.objects.get(name_cat=data['name_cat'].lower()).id
        print("Категория операции записана в базу")

        recipient = [i.name_recipient.lower() for i in Recipient.objects.all()]
        if not recipient or data['name_recipient'].lower() not in recipient:
            rec = Recipient.objects.create(name_recipient=data['name_recipient'].lower())
        else:
            rec = Recipient.objects.get(name_recipient=data['name_recipient'].lower())
        rec.categories.add(CategoryOperation.objects.get(id=category_id))
        print("Реципиент записан в базу")

        cards = [i.number_card for i in CardUser.objects.all()]
        user_id = TelegramUser.objects.get(telegram_id=data['telegram_id']).id
        if not cards or int(data['number_card']) not in cards:
            banks = [i.name_bank for i in BankCard.objects.all()]
            if all([data['name_bank'].lower() not in i.lower() for i in banks]):
                BankCard.objects.create(name_bank=data['name_bank'].lower())
            bank_id = BankCard.objects.get(name_bank=data['name_bank'].lower()).id
            print("Имя банка записано в базу")

            CardUser.objects.create(number_card=data['number_card'],
                                    name_card=data['name_card'].lower(),
                                    balans_card=data['balans'],
                                    BankCard_CardUser_id=bank_id,
                                    TelegramUser_CardUser_id=user_id)
        elif data['balans'] == CardUser.objects.get(number_card=data['number_card']).balans_card - data[
            'amount_operation']:
            card_user = CardUser.objects.get(number_card=data['number_card'])
            card_user.balans_card = data['balans']
            card_user.save()
            data['name_bank'] = CardUser.objects.get(number_card=data['number_card']).BankCard_CardUser.name_bank
            data['name_card'] = CardUser.objects.get(number_card=data['number_card']).name_card
        else:
            return (f'Ошибка обновления баланса\n'
                    f'Баланс до операции: {CardUser.objects.get(number_card=data["number_card"]).balans_card}\n'
                    f'Сумма по операции: {data["amount_operation"]}\n'
            f'Баланс после операции должен быть: {CardUser.objects.get(number_card=data["number_card"]).balans_card - data["amount_operation"]}\n'
            f'Вы ввели сумму: {data["balans"]}\n'
            f'Разница: {CardUser.objects.get(number_card=data["number_card"]).balans_card} - '
            f'{data["amount_operation"]} - {data["balans"]} = '
            f'{CardUser.objects.get(number_card=data["number_card"]).balans_card - data["amount_operation"] - data["balans"]}')

        card_id = CardUser.objects.get(number_card=data['number_card']).id
        print("Имя и номер карты записаны в базу")

        OperationUser.objects.create(datetime_amount=data['datetime_amount'],
                                     amount_operation=data['amount_operation'],
                                     CardUser_OperationUser_id=card_id,
                                     CategoryOperation_OperationUser_id=category_id)
        operation_id = OperationUser.objects.last().id
        print(f"Операция записана в базу\n"
              f"ID операции: {operation_id}")

    except Exception as err:
        print(err)
        return False
    return operation_id
