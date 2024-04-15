import json
import pickle

import pandas as pd
from autocorrect import Speller
from gensim.models import Word2Vec
import gensim
from sklearn.metrics import classification_report, f1_score
from consts import profession_list_without

with open('test.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)
x_test = pd.array(list(control_words.keys()))
y_test = pd.array(list(control_words.values()))


def check_gensim():
    model = gensim.models.KeyedVectors.load('../../model_three_213/model.model')
    y_pred = []
    spell = Speller('ru')

    for j, i in enumerate(x_test):
        word = model.wv.most_similar_to_given(spell(i), profession_list_without)
        y_pred.append(word)
    return y_pred


def check_logist():
    model_name = 'trained_model_v2.sav'
    model = pickle.load(open(model_name, 'rb'))
    return model.predict(x_test)


y_pred = check_logist()
final = classification_report(y_test, y_pred, labels=profession_list_without)
print(final)
print(f"F1 Score: {f1_score(y_test, y_pred, average='weighted')}")

# model = gensim.models.KeyedVectors.load('model_two_187/model.model')
