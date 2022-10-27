# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в vk-группе."""

import logging
import os
import random

from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

import dialogflow_agent
from telegram_log_handler import TelegramLogsHandler


logger = logging.getLogger('support_bot.logger')


def reply(event, vk_api, google_cloud_project):
    """Отвечает в чате VK на сообщение пользователя."""

    dialogflow_session_id = event.user_id
    user_message = event.text
    dialogflow_answer, dialogflow_is_fallback = (
        dialogflow_agent.get_response(
            google_cloud_project,
            dialogflow_session_id,
            user_message
        )
    )
    if dialogflow_is_fallback:
        return

    vk_api.messages.send(
        peer_id=event.peer_id,
        message=dialogflow_answer,
        random_id=random.randint(1, 1000)
    )


def main() -> None:
    """Запускает telegram-бота, использующего DialogFlow."""

    load_dotenv()
    tg_bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    tg_moderator_chat_id = os.environ['TELEGRAM_MODERATOR_CHAT_ID']

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot_token, tg_moderator_chat_id))

    try:
        vk_session = VkApi(token=os.environ['VK_GROUP_TOKEN'])
        vk_api = vk_session.get_api()
        longpoll = VkLongPoll(vk_session)
        google_cloud_project = os.environ['GOOGLE_CLOUD_PROJECT']

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, google_cloud_project)
    except Exception as error:
        logger.exception(f'Ошибка {error} в vk-боте.')


if __name__ == '__main__':
    main()
