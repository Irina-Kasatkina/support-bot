# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в vk-группе."""

import logging
import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

import dialogflow_agent


logger = logging.getLogger('support_bot.logger')


def echo(event, vk_api):
    vk_api.messages.send(
        peer_id=event.peer_id,
        message=event.text,
        random_id=random.randint(1,1000)
    )


def main() -> None:
    """Запускает telegram-бота, использующего DialogFlow."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    vk_session = vk.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)           


if __name__ == '__main__':
    main()
