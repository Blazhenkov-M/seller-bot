from aiogram.fsm.state import State, StatesGroup


class AddAdminState(StatesGroup):
    waiting_for_username = State()


class RemoveAdminState(StatesGroup):
    waiting_for_username = State()


class Newsletter(StatesGroup):
    message = State()


class EditPriceState(StatesGroup):
    subscription = State()
    consultation = State()


class EditMessageState(StatesGroup):
    start = State()
    load_report = State()


class ReportStates(StatesGroup):
    waiting_for_file = State()
    entering_amount = State()
    confirmation = State()
