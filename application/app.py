import pickle
import re
import argparse
import pandas as pd

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


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


def work_with_table(args):

    model_name = 'trained_model_v3.sav'
    model = pickle.load(open(model_name, 'rb'))

    try:
        data = pd.read_excel(args.file, sheet_name=args.sheet)
    except Exception as ex:
        print(f'{Fore.RED}{ex}{Style.RESET_ALL}')
        return

    if args.positions not in data:
        print(f'{Fore.RED}[Errno 2] The column with the name "{args.positions}" does not exist in the sheet{Style.RESET_ALL}')
        return
    if args.enlarged_position not in data:
        print(f'{Fore.RED}[Errno 2] The column with the name "{args.enlarged_position}" does not exist in the sheet{Style.RESET_ALL}')
        return
    data[args.enlarged_position] = None

    for index, row in data.iterrows():
        class_pred = model.predict(clear(row[args.positions]))
        data.loc[index, args.enlarged_position] = class_pred[0]

    data.to_excel("output.xlsx", sheet_name=args.sheet, index=False)
    print(f'{Fore.GREEN}The updated data is written to the "output.xlsx" file{Style.RESET_ALL}')


def main():
    parser = argparse.ArgumentParser(description='Classification Positions')
    parser.add_argument('file', type=str, help='Input dir for Excel file')
    parser.add_argument('sheet', type=str, help='The name of the table being processed')
    parser.add_argument('positions', type=str, help='The column to classify', default='Должность')
    parser.add_argument('enlarged_position', type=str,
                        help='The column in which to record the result of the work',
                        default='Укрупненная должность')

    args = parser.parse_args()
    work_with_table(args)


main()
