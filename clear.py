import pandas as pd
import json
import re
from autocorrect import Speller


def create_dict():
    data = pd.read_excel('positions.xlsx')
    az = set(data['Укрупненная должность'])
    data_profession = {}
    data_reverse_profession = {}
    for i, j in enumerate(az):
        data_profession[j] = i
        data_reverse_profession[i] = j


def create_json():
    data = pd.read_excel('positions.xlsx', sheet_name='Контрольная выборка')
    words = data.to_dict('index')
    final_dict = {}
    for _, i in words.items():
        final_dict[i['Должность']] = i['Укрупненная должность']

    with open('data_control.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=4)


def remove_text_between_parens(text):
    n = 1  # run at least once
    while n:
        text, n = re.subn(r'\([^()]*\)', '', text)  # remove non-nested/flat balanced parts
    return text


def clear(data):
    clear_data = {}
    for word, item in data.items():
        new_check = []
        words_in = remove_text_between_parens(word).split()
        for text in words_in:
            if len(text) <= 2:
                pass
            else:
                new_check.append(text.lower().replace('.', ''))
        clear_word = ' '.join(new_check)
        clear_data[clear_word] = item
    return clear_data


def pre_clear():
    with open('data_control.json', 'r', encoding='utf-8') as json_file:
        words = json.load(json_file)

    new_words = clear(words)
    with open('data_control_clear.json', 'w', encoding='utf-8') as f:
        json.dump(new_words, f, ensure_ascii=False, indent=4)


def speller(data):
    spell = Speller('ru')
    for word, item in data.items():
        print(spell(word), ' - ', word)


data = pd.read_excel('positions_no_repit.xlsx', sheet_name='Лист5')
words = data.to_dict('index')
final_dict = {}
dictionary = {}
for _, i in words.items():
    dictionary[i['Должность']] = i['Укрупненная должность']

with open('new_profession.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False, indent=4)