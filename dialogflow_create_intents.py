# coding=utf-8

import json
import os

from dotenv import load_dotenv
from google.cloud import dialogflow
from translate import Translator


def create_intent(project_id: str, display_name: str, training_phrases_parts: list, message_texts: list) -> None:
    """Создаёт DialogFlow intent заданного типа."""

    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)
    print(message)
    print(type(message))

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = dialogflow.IntentsClient().create_intent(
        request={'parent': dialogflow.AgentsClient.agent_path(project_id), 'intent': intent}
    )
    print(f'Создан интент "{response}"')


def main() -> None:
    load_dotenv()
    project_id = os.environ['DIALOGFLOW_PROJECT_ID']

    translator= Translator(from_lang='russian',to_lang='english')
    with open('questions.json', 'r', encoding='utf-8') as json_file:
        questions_sections = json.load(json_file)

    for questions_section_name, questions_section_details in questions_sections.items():
        translation = translator.translate(questions_section_name)
        display_name = ''.join([word for word in translation.title().split() if len(word) > 2])
        training_phrases_parts = questions_section_details['questions']
        message_texts = [questions_section_details['answer']]
        create_intent(project_id, display_name, training_phrases_parts, message_texts)


if __name__ == '__main__':
    main()