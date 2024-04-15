import asyncio
import os
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from pathlib import Path
from settings import bot
from consts import *
from additiional import *

router = Router()


@router.message(Command("cancel"))
@router.message(F.text == 'Отмена')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
    )


@router.message(Command("check"))
@router.message(F.text == 'Начать')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.answer("Пришлите файл для обработки")
    await state.set_state(ProcessingTable.table)


@router.message(ProcessingTable.table)
async def process_table(message: types.Message, state: FSMContext):
    if getattr(message.document, 'file_name', None) is None:
        await message.answer("Пришлите файл для обработки, попробуйте снова")
        await asyncio.sleep(0.1)
    elif message.document.file_name.split('.')[-1] not in FILE_PERMISSIONS:
        await message.answer(f"Файл должен иметь расширения из списка: {', '.join(FILE_PERMISSIONS)}")
        await asyncio.sleep(0.1)
    else:
        try:
            file = await bot.get_file(message.document.file_id)
            file_path = file.file_path
            personal_path = f'{PATH_FILES}/{message.from_user.id}'
            if not Path(personal_path).exists():
                os.makedirs(personal_path, exist_ok=True)

            name_book = f'{message.message_id}_{message.document.file_name}'
            treatment_id = f'{message.from_user.id}_{message.message_id}'

            await bot.download_file(file_path, f'{personal_path}/{name_book}')
            await state.update_data({
                'id': treatment_id,
                'book': f'{message.from_user.id}/{name_book}'
            })

            await message.answer(f"""Файл получен ✅
Выберите книгу, которую будем обрабатывать:""",
                                 reply_markup=key_books_in_book(treatment_id,
                                                                get_books(f'{personal_path}/{name_book}')))

            await state.set_state(ProcessingTable.book)
        except Exception:
            await message.answer(f"Произошла ошибка, попробуйте позже")
            await asyncio.sleep(0.1)


@router.callback_query(F.data.startswith("book_"))
async def process_book(callback: types.CallbackQuery, state: FSMContext):
    station = await state.get_state()
    data = await state.get_data()
    names = callback.data.split('@')
    if station == ProcessingTable.book and 'id' in data and data['id'] == names[0][5:]:
        await state.update_data({'name_book': names[1]})
        await state.set_state(ProcessingTable.cell_input)
        await callback.message.edit_text(text=f"""Выбрана книга {names[1]}
Теперь выберите название ячейки, которую нужно привести в соответствие:""",
                    reply_markup=key_input_cell(data['id'],
                        get_cells_books(f'{PATH_FILES}/{data["book"]}', names[1])))
    else:
        await callback.message.answer('Обработка еще не начата')


@router.callback_query(F.data.startswith("inputCell_"))
async def process_cell_input(callback: types.CallbackQuery, state: FSMContext):
    station = await state.get_state()
    data = await state.get_data()
    names = callback.data.split('@')
    if station == ProcessingTable.cell_input and 'id' in data and data['id'] == names[0][10:]:
        sells = get_cells_books(f'{PATH_FILES}/{data["book"]}', data['name_book'])
        name_sell = sells[int(names[1])]
        await state.update_data({'id_sell': int(names[1]), 'cell_input': name_sell})
        sells.pop(int(names[1]))
        await callback.message.edit_text(text=f"""Выбрана ячейка <b>{name_sell}</b>
Теперь выберите название ячейки, в которую вставятся укрупненные данные:

<b>Внимание! Прошлый данные в данном столбце будут удалены</b>""",
                                         reply_markup=key_output_cell(data['id'], sells))

        await state.set_state(ProcessingTable.cell_output)
    else:
        await callback.message.answer('Обработка еще не начата')


@router.callback_query(F.data.startswith("outputCell_"))
async def process_cell_output(callback: types.CallbackQuery, state: FSMContext):
    station = await state.get_state()
    data = await state.get_data()
    names = callback.data.split('@')
    if station == ProcessingTable.cell_output and 'id' in data and data['id'] == names[0][11:]:
        await callback.message.edit_text(text='Производим обработку')
        work_with_table(data, int(names[1]))
        file = FSInputFile(f'{PATH_FILES}/{data["book"]}',
                           f"output_{''.join(data['book'].split('/')[1].split('_')[1:])}")
        await bot.send_document(chat_id=callback.message.chat.id, document=file)
        await state.clear()

        await callback.message.delete()
    else:
        await callback.message.answer('Обработка еще не начата')
