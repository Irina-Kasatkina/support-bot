# coding=utf-8

"""Содержит функции взаимодействия с DialogFlow."""

import logging
import os

from google.cloud import dialogflow

import dialogflow_agent


LANGUAGE_CODE = 'ru'


logger = logging.getLogger('support_bot.logger')


def get_response(project_id: str, session_id: str, text: str) -> str:
    """Получает от DialogFlow ответ на реплику пользователя."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text
