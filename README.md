# Telegram-бот, обученный нейросетью

Проект представляет собой Telegram-бота поддержки клиентов вымышленного издательства "Игра глаголов".

## Установка

Для запуска скриптов вам понадобится Python версии 3.8.

Скачайте код с GitHub.

Для управления зависимостями Python желательно воспользоваться [virtualenv](https://pypi.org/project/virtualenv/).

Установите зависимости с помощью `pip` (или `pip3`, есть конфликт с Python2):
```
pip install -r requirements.txt
```

### Переменные окружения

Часть настроек утилит берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в той же папке, где и скрипты, и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступно 3 обязательныхя переменных:

- `TELEGRAM_BOT_TOKEN` - API-токен telegram-бота, с помощью которого будет осуществляться отправка уведомлений. Например: `TELEGRAM_BOT_TOKEN=958423683:AAEAtJ5Lde5YYfkjergber`. Если такого telegram-бота пока нет, [создайте его](https://way23.ru/регистрация-бота-в-telegram.html).

- `DIALOGFLOW_PROJECT_ID` - идентификатор проекта DialogFlow ([Инструкция по созданию](https://cloud.google.com/dialogflow/es/docs/quick/setup)). Например: `DIALOGFLOW_PROJECT_ID=moulin-start-55`.

- `GOOGLE_APPLICATION_CREDENTIALS` - путь к json-файлу с Application Default Credentials ([см. инструкцию по созданию](https://cloud.google.com/docs/authentication/client-libraries)).

## Запуск

Для запуска скрипта откройте консоль `cmd`, перейдите в директорию со скриптом с помощью команды `cd` и наберите в командной строке команду:
```
python support-bot.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
