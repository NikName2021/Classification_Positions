import pandas as pd
import re
import pickle

from consts import PATH_FILES, PATH_MODEL


def get_books(path):
    xlsx = pd.ExcelFile(path)
    sheet_names = xlsx.sheet_names
    xlsx.close()
    return sheet_names


def get_cells_books(path, book):
    df = pd.read_excel(path, sheet_name=book)
    return list(df)

def remove_text_between_parens(text):
    n = 1
    while n:
        text, n = re.subn(r'\([^()]*\)', '', text)
    return text


def clear(word):
    new_check = []
    words_in = remove_text_between_parens(word).split()
    for text in words_in:
        if len(text) <= 2:
            pass
        else:
            new_check.append(text.lower().replace('.', ''))
    clear_word = ' '.join(new_check)

    return [clear_word]


def work_with_table(args, output):

    model = pickle.load(open(PATH_MODEL, 'rb'))

    data = pd.read_excel(f'{PATH_FILES}/{args["book"]}', sheet_name=args['name_book'])
    sells = list(data)
    sells.pop(args['id_sell'])
    update_sell = sells[output]
    data[update_sell] = None

    for index, row in data.iterrows():
        class_pred = model.predict(clear(row[args['cell_input']]))
        data.loc[index, update_sell] = class_pred[0]

    writer = pd.ExcelWriter(f'{PATH_FILES}/{args["book"]}', engine='openpyxl', mode='a', if_sheet_exists='replace')
    data.to_excel(writer, sheet_name=args['name_book'], index=False)
    writer.close()