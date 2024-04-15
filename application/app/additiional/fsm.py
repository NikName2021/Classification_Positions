from aiogram.fsm.state import StatesGroup, State


class ProcessingTable(StatesGroup):
    table = State()
    book = State()
    cell_input = State()
    cell_output = State()


