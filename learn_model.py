from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import f1_score
import json
import pickle
import pandas as pd
from consts import profession_list_without


with open('train_2.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)
x_train = list(control_words.keys())
y_train = list(control_words.values())


with open('test_2.json', 'r', encoding='utf-8') as json_file:
    control_words = json.load(json_file)
x_test = pd.array(list(control_words.keys()))
y_test = pd.array(list(control_words.values()))


logreg = Pipeline([
    ('vect', CountVectorizer(analyzer='char', ngram_range=(2, 10))),
    ('tfidf', TfidfTransformer()),
    ('clf', LogisticRegression(n_jobs=3, C=1e5, solver='saga',
                               multi_class='multinomial',
                               max_iter=1000,
                               random_state=42)),
])

logreg.fit(x_train, y_train)
model_name = 'trained_model_v3.sav'
pickle.dump(logreg, open(model_name, 'wb'))

y_pred = logreg.predict(x_test)

print(classification_report(y_test, y_pred, labels=profession_list_without))
print(f"F1 Score: {f1_score(y_test, y_pred, average='weighted')}")
