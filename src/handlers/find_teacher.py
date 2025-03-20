from datetime import datetime

from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.find_teacher import find_teacher_keyboard, build_teacher_list_kb, try_again_name_kb, build_date_change_keyboard, build_days_keyboard, build_teacher_schedule_month_keyboard
from utils.message_generators import generate_teacher_schedule_message
from utils.api.schedule import LessonAPI, TeacherAPI

router = Router()

class FindTeacher(StatesGroup):
    teacher_name = State()

async def get_teacher_list(name: str = ''):
    resp = await TeacherAPI.get()
    teachers = resp.json
    if name:
        teachers = [teacher for teacher in teachers if name.lower() in teacher.get('short_name').lower()]
    return teachers

async def get_teacher_schedule(teacher_id: int, date: str):
    date = datetime.strptime(date, '%Y-%m-%d')
    resp = await LessonAPI.get(teacher_id=teacher_id, date=date)
    lessons = resp.json
    new_lessons = {}
    resp = await TeacherAPI.get(teacher_id=teacher_id)
    teacher = resp.json[0]
    for lesson in lessons:
        time = lesson.get('time_from')
        if not new_lessons.get(time):
            new_lessons[time] = lesson
    message = await generate_teacher_schedule_message(sorted(new_lessons.values(), key=lambda x: x.get('time_from')), date, teacher)
    keyboard = await build_date_change_keyboard(date, teacher_id)
    return message, keyboard

@router.message(F.text == '🔍 Найти преподавателя')
async def find_teacher(message: types.Message):
    await message.answer(
        '🔍 <b>Не можете найти преподавателя?</b>\n\n'
        'Вы можете узнать, на каком занятии сейчас находится преподаватель, '
        'чтобы не ждать около кабинета или не тратить время на поиски.\n\n'
        '<b>Внимание!</b> Поиск преподавателя работает на основе расписания. То есть мы не можем сказать где находится преподаватель, если у него нету пар\n\n'
        'Введите фамилию преподавателя или выберите его из списка для начала поиска.',
        reply_markup=find_teacher_keyboard.as_markup(),
    )

@router.callback_query(F.data == 'teacher_name')
async def get_teacher_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введите фамилию преподавателя')
    await state.set_state(FindTeacher.teacher_name)

@router.message(FindTeacher.teacher_name)
async def get_teacher_list_by_name(message: types.Message, state: FSMContext):
    teacher_name = message.text
    await state.clear()
    teachers = await get_teacher_list(name=teacher_name)
    if not teachers:
        await message.answer('По вашему запросу ничего не найдено', reply_markup=try_again_name_kb.as_markup())
        return
    kb = await build_teacher_list_kb(teachers, teacher_filter=teacher_name)
    await message.answer('Выберите преподавателя', reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith('teacher_list_'))
async def get_full_teacher_list(callback: types.CallbackQuery):
    teacher_filter, page = callback.data.split('_')[-2:]
    teachers = await get_teacher_list(name=teacher_filter)
    kb = await build_teacher_list_kb(teachers, page=int(page), teacher_filter=teacher_filter)
    await callback.message.edit_text('Выберите преподавателя', reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith('get_teacher_schedule_'))
async def get_teacher_schedule_from_inline(callback: types.CallbackQuery):
    teacher_id, date = callback.data.split('_')[-2:]
    message, kb = await get_teacher_schedule(teacher_id=int(teacher_id), date=date)
    await callback.message.edit_text(message, reply_markup=kb.as_markup())


@router.callback_query(F.data.startswith('teacher_schedule_date_choice'))
async def schedule_date_choice(callback: types.CallbackQuery):
    teacher_id = callback.data.split('_')[-1]
    kb = await build_teacher_schedule_month_keyboard(teacher_id=int(teacher_id))
    await callback.message.edit_text('Выберите месяц', reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith('teacher_schedule_month_set'))
async def schedule_month_set(callback: types.CallbackQuery):
    teacher_id, month_index = callback.data.split('_')[-2:]
    kb = await build_days_keyboard(int(month_index), teacher_id=int(teacher_id))
    await callback.message.edit_text('Выберите день', reply_markup=kb.as_markup())
