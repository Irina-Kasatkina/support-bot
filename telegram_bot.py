# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в telegram-чате."""

import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

import dialogflow_agent


logger = logging.getLogger('support_bot.logger')


def start_command(update: Update, context: CallbackContext) -> None:
    """Посылает в telegram-чат сообщение, когда пользователь ввёл команду /start."""

    update.message.reply_text('Здравствуйте!')


def reply(update: Update, context: CallbackContext, google_cloud_project: str) -> None:
    """Отвечает в telegram-чате на сообщение пользователя."""

    dialogflow_session_id = update.effective_chat.id
    user_message = update.message.text
    dialogflow_response = dialogflow_agent.get_response(
        google_cloud_project,
        dialogflow_session_id,
        user_message
    )
    update.message.reply_text(dialogflow_response.query_result.fulfillment_text)


def main() -> None:
    """Запускает telegram-бота, использующего DialogFlow."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()

    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & ~Filters.command,
            partial(reply, google_cloud_project=os.environ['GOOGLE_CLOUD_PROJECT'])
        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
