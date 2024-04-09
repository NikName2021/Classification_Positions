import json

import pandas as pd
from sklearn.model_selection import train_test_split

with open('data_clear.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)

with open('data_control_clear.json', 'r', encoding='utf-8') as json_file:
    augment = json.load(json_file)

dictionary = dict(list(control_words.items()) + list(augment.items()))

x_train = pd.array(list(dictionary.keys()))
y_train = pd.array(list(dictionary.values()))


X_train, X_test, y_train, y_test = train_test_split(x_train, y_train, train_size=0.7,
                                                    random_state=42)

test_dict = {}
train_dict = {}

for i, j in enumerate(X_train):
    train_dict[j] = y_train[i]

for i, j in enumerate(X_test):
    test_dict[j] = y_test[i]

with open('train.json', 'w', encoding='utf-8') as f:
    json.dump(train_dict, f, ensure_ascii=False, indent=4)

with open('test.json', 'w', encoding='utf-8') as f:
    json.dump(test_dict, f, ensure_ascii=False, indent=4)
