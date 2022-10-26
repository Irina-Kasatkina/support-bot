# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в telegram-чате."""

import logging
import os
from functools import partial

from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

import dialogflow_agent


LANGUAGE_CODE = 'ru'


logger = logging.getLogger('support_bot.logger')


def start_command(update: Update, context: CallbackContext) -> None:
    """Посылает в telegram-чат сообщение, когда пользователь ввёл команду /start."""

    update.message.reply_text('Здравствуйте!')


def reply(update: Update, context: CallbackContext, dialogflow_project_id: str) -> None:
    """Отвечает в telegram-чате на сообщение пользователя."""

    dialogflow_session_id = update.effective_chat.id
    user_message = update.message.text
    dialogflow_response = dialogflow_agent.get_response(
        dialogflow_project_id,
        dialogflow_session_id,
        user_message
    )
    update.message.reply_text(dialogflow_response)


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
            partial(reply, dialogflow_project_id=os.environ['DIALOGFLOW_PROJECT_ID'])
        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
