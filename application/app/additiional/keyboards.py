from aiogram import types


def key_start():
    kb = [
        [types.KeyboardButton(text="Начать")],
        [types.KeyboardButton(text="Отмена")]
    ]
    return types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)


def key_books_in_book(id_mess, books):
    buttons = []
    for book in books:
        buttons.append([types.InlineKeyboardButton(text=f"{book}", callback_data=f"book_{id_mess}@{book}")])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def key_input_cell(id_mess, names):
    buttons = []
    for i, name in enumerate(names):
        buttons.append([types.InlineKeyboardButton(text=f"{name[:20]}", callback_data=f"inputCell_{id_mess}@{i}")])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)


def key_output_cell(id_mess, names):
    buttons = []
    for i, name in enumerate(names):
        buttons.append([types.InlineKeyboardButton(text=f"{name}", callback_data=f"outputCell_{id_mess}@{i}")])
    return types.InlineKeyboardMarkup(inline_keyboard=buttons)
