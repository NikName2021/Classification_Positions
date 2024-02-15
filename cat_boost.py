from catboost import CatBoostClassifier, Pool
import pandas as pd
import json
from consts import profession_list


def fit_model(x_learn, y_learn, test_pool, **kwargs):
    model = CatBoostClassifier(task_type='CPU', iterations=5000,
                               eval_metric='TotalF1', od_type='Iter',
                               od_wait=500, **kwargs)

    return model.fit(x_learn, y_learn, eval_set=test_pool,
                     verbose=100, plot=True,
                     use_best_model=True)


with open('data_clear.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)
x_train = list(control_words.keys())
y_train = list(control_words.values())

with open('data_control_clear.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)
x_test = list(control_words.keys())
y_test = list(control_words.values())

# train_pool = Pool(data=x_train, label=y_train)
# valid_pool = Pool(data=x_test, label=y_test,
#                   text_features=profession_list)

model = fit_model(x_train, y_train, (x_test, y_test), learning_rate=0.35,
                  dictionaries=[{
                      'dictionary_id': 'Word',
                      'max_dictionary_size': '50000'
                  }],
                  feature_calcers=['BoW:top_tokens_count=10000'])
