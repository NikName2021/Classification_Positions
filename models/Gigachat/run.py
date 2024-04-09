import os

import requests
import uuid
import json
from time import sleep
from sklearn.metrics import classification_report, f1_score
from consts import profession_list, profession_list_without, TEST_PATH_V1
from dotenv import load_dotenv


def get_token(auth_token, scope='GIGACHAT_API_PERS'):
    """
      Выполняет POST-запрос к эндпоинту, который выдает токен.

      Параметры:
      - auth_token (str): токен авторизации, необходимый для запроса.
      - scope (str): область действия запроса API. По умолчанию — «GIGACHAT_API_PERS».

      Возвращает:
      - ответ API, где токен и срок его "годности".
      """
    # Создадим идентификатор UUID (36 знаков)
    rq_uid = str(uuid.uuid4())

    # API URL
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    # Заголовки
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {auth_token}'
    }

    # Тело запроса
    payload = {
        'scope': scope
    }

    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        return response
    except requests.RequestException as e:
        print(f"Ошибка: {str(e)}")
        return -1


def get_chat_completion(auth_token, user_message, conversation_history=None):
    """
    Отправляет POST-запрос к API чата для получения ответа от модели GigaChat в рамках диалога.

    Параметры:
    - auth_token (str): Токен для авторизации в API.
    - user_message (str): Сообщение от пользователя, для которого нужно получить ответ.
    - conversation_history (list): История диалога в виде списка сообщений (опционально).

    Возвращает:
    - response (requests.Response): Ответ от API.
    - conversation_history (list): Обновленная история диалога.
    """
    # URL API, к которому мы обращаемся
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Если история диалога не предоставлена, инициализируем пустым списком
    if conversation_history is None:
        conversation_history = []

    # # Добавляем сообщение пользователя в историю диалога
    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    # Подготовка данных запроса в формате JSON
    payload = json.dumps({
        "model": "GigaChat",
        "messages": conversation_history,
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1,
        "update_interval": 0
    })

    # Заголовки запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {auth_token}'
    }

    # Выполнение POST-запроса и возвращение ответа
    try:
        response = requests.post(url, headers=headers, data=payload, verify=False)
        response_data = response.json()

        # Добавляем ответ модели в историю диалога
        conversation_history.append({
            "role": "assistant",
            "content": response_data['choices'][0]['message']['content']
        })

        return response, conversation_history
    except requests.RequestException as e:
        # Обработка исключения в случае ошибки запроса
        print(f"Произошла ошибка: {str(e)}")
        return None, conversation_history


def run():
    load_dotenv()
    response = get_token(os.getenv('AUTH_DATA'))
    # print(response)
    if response != 1:
        print(response.text)
    giga_token = response.json()["access_token"]

    conversation_history = [{
        'role': 'system',
        'content': f'Ты бот, который должен классифицировать данную тебе должность, ты можешь отвечать ТОЛЬКО ДОЛЖНОСТЬЮ ИЗ СПИСКА: {", ".join(profession_list)}'
    }]
    with open(TEST_PATH_V1, 'r', encoding='utf-8') as json_file:
        control_words = json.load(json_file)

    prediction = []
    test = []
    for i, j in control_words.items():
        response, conversation_history = get_chat_completion(giga_token, i, conversation_history)
        answer = response.json()['choices'][0]['message']['content']

        test.append(j)
        prediction.append(answer)

        print(answer, j)
        sleep(1)

    print(classification_report(test, prediction, labels=profession_list_without))
    print(f"F1 Score: {f1_score(test, prediction, average='weighted')}")


if __name__ == '__main__':
    run()
