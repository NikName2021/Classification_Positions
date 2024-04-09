import json

import pandas as pd
from sklearn.model_selection import train_test_split

with open('train.json', 'r', encoding='utf-8') as json_file:
    test = json.load(json_file)

with open('test.json', 'r', encoding='utf-8') as json_file:
    train = json.load(json_file)

with open('new_profession.json', 'r', encoding='utf-8') as json_file:
    new_professions = json.load(json_file)

with open('new_data.json', 'r', encoding='utf-8') as json_file:
    new_data = json.load(json_file)

dictionary = dict(list(test.items()) + list(train.items()) + list(new_professions.items()) + list(new_data.items()))

x_data = pd.array(list(dictionary.keys()))
y_data = pd.array(list(dictionary.values()))

X_train, X_test, y_train, y_test = train_test_split(x_data, y_data, train_size=0.7,
                                                    random_state=42)

test_dict = {}
train_dict = {}

for i, j in enumerate(X_train):
    train_dict[j] = y_train[i]

for i, j in enumerate(X_test):
    test_dict[j] = y_test[i]

print(len(test_dict.keys()))
print(len(train_dict.keys()))

with open('train_2.json', 'w', encoding='utf-8') as f:
    json.dump(train_dict, f, ensure_ascii=False, indent=4)

with open('test_2.json', 'w', encoding='utf-8') as f:
    json.dump(test_dict, f, ensure_ascii=False, indent=4)
