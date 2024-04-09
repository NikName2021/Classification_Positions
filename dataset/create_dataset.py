import random
import pandas as pd
import json
import csv

letters = list('ёйфяцычувскамепинртгоьшлбюджэъхзщ ')


def create_random():
    data = pd.read_excel('positions_no_repit.xlsx', sheet_name='Лист2')
    words = data.to_dict('index')
    final_dict = {}
    dictionary = {}
    for _, i in words.items():
        dictionary[i['Должность']] = i['Укрупненная должность']

    for word, classion in dictionary.items():
        word = word.lower()
        for i in range(4):
            index = random.randrange(0, len(word) - 1)
            final_dict[word[:index] + random.choice(letters) + word[index:]] = classion

        for i in range(4):
            index = random.randrange(0, len(word) - 1)
            final_dict[word[:index] + word[index + 1:]] = classion

    with open('new_data.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=4)


def find_sin():
    data = pd.read_excel('positions_no_repit.xlsx', sheet_name='Лист3')
    words = data.to_dict('index')
    final_dict = {}
    dictionary = {}
    for _, i in words.items():
        if type(i['Должность']) is str:
            dictionary[i['Должность'].lower()] = i['Укрупненная должность']

    with open('professions.csv', newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';')
        for row in spamreader:
            for word, cls in dictionary.items():
                if word in row[1].lower():
                    final_dict[row[1].lower()] = cls
    print(len(final_dict))
    with open('new_profession.json', 'w', encoding='utf-8') as f:
        json.dump(final_dict, f, ensure_ascii=False, indent=4)

    audit = {}
    for word, cls in final_dict.items():
        if cls in audit:
            audit[cls] += 1
        else:
            audit[cls] = 1
    print(audit)
