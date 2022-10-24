# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в telegram-чате."""

import logging
import os

from dotenv import load_dotenv
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


logger = logging.getLogger('support_bot.logger')


def start_command(update: Update, context: CallbackContext) -> None:
    """Посылает сообщение, когда клиент ввёл команду /start."""

    context.bot.send_message(chat_id=update.effective_chat.id, text="Здравствуйте!")


def echo(update: Update, context: CallbackContext) -> None:
    """Повторяет сообщение клиента."""

    update.message.reply_text(update.message.text)


def main() -> None:
    """Запускает бота."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    telegram_bot_token = os.environ['TELEGRAM_BOT_TOKEN']

    updater = Updater(telegram_bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
