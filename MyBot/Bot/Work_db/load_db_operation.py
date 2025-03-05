import logging
from asgiref.sync import sync_to_async

from Bot.models import TypeOperation, CategoryOperation, Recipient, BankCard, CardUser, OperationUser, TelegramUser

logger = logging.getLogger(__name__)

@sync_to_async
def load_db_operation(data) -> tuple[int, str] | Exception:
    """
    Обрабатывает данные операции пользователя и сохраняет их в базу данных.

    :param data: Словарь с данными операции.
    :return: Кортеж (ID операции, текстовое представление данных) или исключение.
    """
    try:
        # Логируем входные данные
        logger.info("Обрабатываем данные операции:")
        for key, value in data.items():
            logger.info(f"{key:<15} --- {str(value):<20}")

        # Создаем или получаем тип операции
        type_operation, _ = TypeOperation.objects.get_or_create(
            name_type=data['name_type'].lower()
        )
        logger.info(f"Тип операции '{type_operation.name_type}' записан в базу")

        # Создаем или получаем категорию операции
        category, _ = CategoryOperation.objects.get_or_create(
            name_cat=data['name_cat'].lower(),
            defaults={'type': type_operation}
        )
        logger.info(f"Категория операции '{category.name_cat}' записана в базу")

        # Создаем или получаем получателя
        recipient, created = Recipient.objects.get_or_create(
            name_recipient=data['name_recipient'].lower(),
            defaults={'recipient_in_notification': data.get('recipient_in_notification', False)}
        )

        # Если получатель уже существовал и поле recipient_in_notification передано, обновляем его
        if not created and 'recipient_in_notification' in data:
            recipient.recipient_in_notification = data['recipient_in_notification']
            recipient.save()

        # Логируем результат
        logger.info(f"Получатель '{recipient.name_recipient}' записан в базу")

        if data.get('name_bank_out', None):
            # Создаем или получаем банк списания
            bank_out, _ = BankCard.objects.get_or_create(
                name_bank=data['name_bank_out'].lower()
            )
            logger.info(f"Банк списания'{bank_out.name_bank}' записан в базу")

        # Создаем или получаем банк зачисления
        bank, _ = BankCard.objects.get_or_create(
            name_bank=data['name_bank'].lower()
        )
        logger.info(f"Банк '{bank.name_bank}' записан в базу")

        # Получаем пользователя
        user = TelegramUser.objects.get(telegram_id=data['telegram_id'])

        if data.get('number_card_out', None):
            # Создаем или обновляем карту списания
            card_out, created_out = CardUser.objects.get_or_create(
                number_card=data['number_card_out'],
                defaults={
                    'name_card': data['name_card_out'].lower(),
                    'balans_card': data['balans_out'],
                    'bank': bank_out,
                    'telegram_user': user,
                    'credit_limit': data['credit_limit_out'],
                    'type_card': data['type_card_out'],
                    'currency_card': data['currency_card_out'],
                }
            )
            if not created_out and data.get('number_card_out', None):
                # Обновляем баланс карты списания
                if data['balans_out'] == card_out.balans_card - data['amount_operation_out']:
                    card_out.balans_card = data['balans_out']
                    card_out.save()
                elif data['balans_out'] == card_out.balans_card + data['amount_operation_out']:
                    card_out.balans_card = data['balans_out']
                    card_out.save()
                else:
                    error_message = (
                        f'Ошибка обновления баланса карты списания\n'
                        f'Баланс до операции: {card_out.balans_card}\n'
                        f'Сумма по операции: {data["amount_operation_out"]}\n'
                        f'Баланс после операции должен быть: {card_out.balans_card - data["amount_operation_out"]}\n'
                        f'Вы ввели сумму: {data["balans_out"]}\n'
                        f'Разница: {card_out.balans_card} - {data["amount_operation_out"]} - {data["balans_out"]} = '
                        f'{card_out.balans_card - data["amount_operation_out"] - data["balans_out"]}'
                    )
                    logger.error(error_message)
                    return ValueError(error_message)
            logger.info(f"Карта списания'{card_out.name_card}-{card_out.number_card}' записана в базу")
        # Создаем или обновляем карту
        card, created = CardUser.objects.get_or_create(
            number_card=data['number_card'],
            defaults={
                'name_card': data['name_card'].lower(),
                'balans_card': data['balans'],
                'bank': bank,
                'telegram_user': user,
                'credit_limit': data['credit_limit'],
                'type_card': data['type_card'],
                'currency_card': data['currency_card']
            }
        )
        if not created:
            # Обновляем баланс карты
            if data['balans'] == card.balans_card - data['amount_operation']:
                card.balans_card = data['balans']
                card.save()
            elif data['balans'] == card.balans_card + data['amount_operation']:
                card.balans_card = data['balans']
                card.save()
            else:
                error_message = (
                    f'Ошибка обновления баланса\n'
                    f'Баланс до операции: {card.balans_card}\n'
                    f'Сумма по операции: {data["amount_operation"]}\n'
                    f'Баланс после операции должен быть: {card.balans_card - data["amount_operation"]}\n'
                    f'Вы ввели сумму: {data["balans"]}\n'
                    f'Разница: {card.balans_card} - {data["amount_operation"]} - {data["balans"]} = '
                    f'{card.balans_card - data["amount_operation"] - data["balans"]}'
                )
                logger.error(error_message)
                return ValueError(error_message)
        logger.info(f"Карта '{card.name_card}-{card.number_card}' записана в базу")

        # Формируем текстовое представление данных
        text = '\n'.join(f'<code>{key:<17} ------ {value}</code>' for key, value in data.items())
        text_note_operation = text.replace('<code>', '').replace('</code>', '')
        if not data.get('note_operation'):
            data['note_operation'] = text_note_operation

        if data.get('number_card_out', None):
            # Создаем операцию списания
            operation_out = OperationUser.objects.create(
                datetime_amount=data['datetime_amount'],
                amount_operation=data['amount_operation_out'],
                balans=data['balans_out'],
                note_operation=data['note_operation'],
                card=card_out,
                category=category,
                recipient=recipient,
            )
        # Создаем операцию зачисления
        operation = OperationUser.objects.create(
            datetime_amount=data['datetime_amount'],
            amount_operation=data['amount_operation'],
            balans=data['balans'],
            note_operation=data['note_operation'],
            card=card,
            category=category,
            recipient=recipient,
        )

        op = ''
        if data.get('number_card_out', None):
            logger.info(f"Операция списания записана в базу. ID операции: {operation_out.id}")
            op += str(operation_out.id) + ", "
        logger.info(f"Операция записана в базу. ID операции: {operation.id}")
        op += str(operation.id)

        return op, text

    except Exception as err:
        logger.error(f"Произошла ошибка при обработке операции: {err}", exc_info=True)
        return err