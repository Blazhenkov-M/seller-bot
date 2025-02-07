from aiogram.fsm.state import State, StatesGroup


class ReportStates(StatesGroup):
    waiting_for_file = State()
    choosing_categories = State()
    entering_amounts = State()
