from asgiref.sync import sync_to_async

from Bot.models import Recipient

@sync_to_async
def get_recipient_db():
    try:
        recipient_lst = [i.name_recipient.capitalize() for i in Recipient.objects.all()]
    except Exception as err:
        return
    return recipient_lst
