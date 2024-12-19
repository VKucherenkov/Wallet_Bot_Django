import logging

logger = logging.getLogger(__name__)

msg1 = (f'[03.12.2024 в 12:07]\n'
       f'Списание за уведомления об операциях\n'
       f'ПЛАТ.СЧЁТ*7473 01:45 Оплата 40р за уведомления по СберКартам. Следующее списание 03.01.25. '
       f'Баланс: 3714,22р.')
msg2 = (f'[18.12.2024 в 08:31]\n'
        f'Покупка MISHA KOFE_VEN\n'
        f'100 ₽\n'
        f'МИР •• 6522\n'
        f'Баланс: 702062,63₽')

for msg in [msg1, msg2]:
       msg_date = msg[msg.index('[') + 1 : msg.index('[') + 1 + 10] + ' ' + msg[msg.index(']') + 1 - 6 : msg.index(']')]
       if 'Списание' in [i for i in msg.split('\n')][1]:
              msg_card = msg[msg.index('*') + 1 : msg.index('*') + 1 + 4]
              msg_seller = [i for i in msg.split('\n')][1]
              msg_amount = [j[:-1] for j in [i for i in msg.split('\n')][2].split() if j[-1] == 'р'][0]
              msg_balance = [i for i in msg.split('\n')][-1].split()[-1][:-2]

       elif 'Покупка' in [i for i in msg.split('\n')][1]:
              msg_card = msg[msg.rindex('•') + 2 : msg.index('•') + 2 + 5]
              msg_seller = ' '.join([i for i in msg.split('\n')][1].split()[1:])
              msg_amount = [i for i in msg.split('\n')][2][:-2]
              msg_balance = [i for i in msg.split('\n')][-1].split()[-1][:-1]

       print(msg, msg_date, msg_card, msg_seller, msg_amount, msg_balance, sep='\n')



