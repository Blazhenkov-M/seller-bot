from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.start import load_xl_kb
from texts import REPORT_UPLOAD_MSG
from states import ReportStates
load_router = Router()


@load_router.message(F.text.lower() == "/upload")
async def trigger_upload(msg: Message):
    await msg.answer("Вы можете загрузить отчет, нажав кнопку ниже:", reply_markup=load_xl_kb)


@load_router.callback_query(F.data == "load_report")
async def load_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(REPORT_UPLOAD_MSG)
    await state.set_state(ReportStates.waiting_for_file)  # FSM переходит в состояние ожидания файла


@load_router.message(ReportStates.waiting_for_file, F.document)
async def process_xl_file(msg: Message, state: FSMContext):
    file = msg.document
    if not file.file_name.endswith((".xls", ".xlsx")):
        await msg.answer("Файл должен быть в формате Excel (.xls или .xlsx).\nПожалуйста, загрузите корректный файл.")
        return

    if file.file_size > 20_000_000:
        await msg.answer("Файл слишком большой! Максимальный размер 20 МБ. Попробуйте снова.")
        return

    await msg.answer("✅ Файл принят!\nТеперь выберите категории расходов.")
    await state.set_state(ReportStates.choosing_categories)


# Обработка НЕ файла (юзер пишет что-то вместо загрузки)
@load_router.message(ReportStates.waiting_for_file)
async def handle_non_file_input(msg: Message):
    await msg.answer("📎 Пожалуйста, прикрепите файл отчёта в формате Excel.")
