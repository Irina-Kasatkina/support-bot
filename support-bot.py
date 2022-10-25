# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в telegram-чате."""

import logging
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram import ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater


LANGUAGE_CODE = 'ru'


logger = logging.getLogger('support_bot.logger')


def start_command(update: Update, context: CallbackContext) -> None:
    """Посылает сообщение, когда клиент ввёл команду /start."""

    update.message.reply_text('Здравствуйте!')


def reply(update: Update, context: CallbackContext) -> None:
    """Отвечает на приветствие клиента."""

    session_id = update.effective_chat.id
    text = update.message.text
    response_text = get_dialoflow_response(session_id, text)
    update.message.reply_text(response_text)


def get_dialoflow_response(session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(os.environ['DIALOGFLOW_PROJECT_ID'], session_id)
    text_input = dialogflow.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text


def main() -> None:
    """Запускает бота."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
