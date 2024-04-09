import json

import requests
from sklearn.metrics import classification_report, f1_score

from consts import profession_list, profession_list_without, TEST_PATH_V1
from dotenv import load_dotenv
import os
import time


def search(res, auth: tuple, categories=profession_list):
    prompt = {
        # "modelUri": "ds://{}",
        "modelUri": f"gpt://{auth[0]}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.1,
            "maxTokens": "2000"
        },
        "messages": [
            {
                "role": "system",
                "text": f'Ты бот, который должен классифицировать данную тебе должность, ты можешь отвечать ТОЛЬКО ДОЛЖНОСТЬЮ ИЗ СПИСКА: {", ".join(categories)}'
            },
            {
                "role": "user",
                "text": res
            },
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {auth[1]}",
        # "x-folder-id": '{folder_id}
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = response.json()
    try:
        final = (result['result']['alternatives'][0]['message']['text'])
    except Exception as ex:
        print(ex, '\n', result)
        final = ''
    return final


def run():
    load_dotenv()
    auth_data = (os.getenv('FOLDER'), os.getenv('API_KEY'))

    with open(TEST_PATH_V1, 'r', encoding='utf-8') as json_file:
        control_words = json.load(json_file)
    prediction = []
    test = []

    for i, j in control_words.items():
        answer = search(i, auth_data)
        print(f"Ответ модели: {answer} -- Ответ: {j}")
        test.append(j)
        if '.' in answer:
            answer = answer.replace('.', '')

        prediction.append(answer)

        time.sleep(5)

    print(classification_report(test, prediction, labels=profession_list_without))
    print(f"F1 Score: {f1_score(test, prediction, average='weighted')}")


if __name__ == '__main__':
    run()
