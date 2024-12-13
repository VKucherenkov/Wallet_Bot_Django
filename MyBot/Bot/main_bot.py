import logging

import telebot

from django.conf import settings

from Bot.db_work import db_telegramuser

bot = telebot.TeleBot(settings.TOKEN_BOT, parse_mode='HTML')

telebot.logger.setLevel(settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    txt = db_telegramuser(message, logger)
    logger.info(f'{txt}')
    logger.info(f'{message.text}')
    text = f'😊 Привет <b>{message.chat.first_name}</b> 😊'
    text_message = (f'😱 Пользователь <b>{message.chat.first_name}</b> с id {message.from_user.id} написал:\n'
                    f'{message.text}')
    bot.send_message(chat_id=message.from_user.id, text=text)
    bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN, text=text_message)



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    msg = message.text
    if 'ПЛАТ.СЧЁТ' in msg:
        msg = msg[msg.index('ПЛАТ.СЧЁТ'):]
    logger.info(f'Имя пользователя = {message.chat.first_name}')
    logger.info(f'id = {message.from_user.id}')
    logger.info(f'{msg = }')
    text_message = (f'😱 Пользователь <b>{message.chat.first_name}</b> с id {message.from_user.id} написал:\n'
                    f'{msg}')
    bot.send_message(chat_id=settings.TELEGRAM_ID_ADMIN, text=text_message)
