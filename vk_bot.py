# coding=utf-8

"""Осуществляет умную поддержку клиентов издательства 'Игра глаголов' в vk-группе."""

import logging
import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType

import dialogflow_agent


logger = logging.getLogger('support_bot.logger')


def main() -> None:
    """Запускает telegram-бота, использующего DialogFlow."""

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()
    vk_session = vk_api.VkApi(token=os.environ['VK_GROUP_TOKEN'])
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()
