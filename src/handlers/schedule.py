
from aiogram import Router, F, types


from datetime import datetime

from keyboards.schedule import build_date_change_keyboard, month_choice_kb, build_days_keyboard
from utils.message_generators import generate_schedule_message
from utils.api.user import StudentAPI
from utils.api.schedule import LessonAPI


schedule_router = Router()

async def get_schedule_data(user_id: int, date: datetime):
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    resp = await LessonAPI.get(group_id=user.get('group_id'), date=date, with_teacher=True)
    lessons = resp.json
    for index in range(len(lessons) - 1, 0, -1):
        if lessons[index].get('time_from') == lessons[index - 1].get('time_from'):
            lessons[index - 1]['cabinet'] += (' | ' + lessons[index].get('cabinet')) if lessons[index].get('cabinet') else ''
            lessons[index - 1]['teacher']['short_name'] += (' | ' + lessons[index]['teacher']['short_name']) if lessons[index].get('teacher') else ''
            del lessons[index]
    generated_message = await generate_schedule_message(lessons, date)
    keyboard = await build_date_change_keyboard(date)

    return generated_message, keyboard

@schedule_router.message(F.text == '📅 Расписание')
async def schedule_from_reply(message: types.Message):
    date = datetime.today()
    user_id = message.from_user.id
    text, keyboard = await get_schedule_data(user_id, date)
    await message.answer(
        text=text,
        reply_markup=keyboard.as_markup(),
    )


@schedule_router.callback_query(F.data.startswith('get_schedule'))
async def schedule_from_inline(callback: types.CallbackQuery):
    str_date = callback.data.split('_')[-1]
    date = datetime.strptime(str_date, '%Y-%m-%d')
    user_id = callback.from_user.id
    text, keyboard = await get_schedule_data(user_id, date)
    await callback.message.edit_text(text=text)
    await callback.message.edit_reply_markup(reply_markup=keyboard.as_markup())

@schedule_router.callback_query(F.data == 'schedule_date_choice')
async def schedule_date_choice(callback: types.CallbackQuery):
    await callback.message.edit_text('Выберите месяц', reply_markup=month_choice_kb.as_markup())

@schedule_router.callback_query(F.data.startswith('schedule_month_set'))
async def schedule_month_set(callback: types.CallbackQuery):
    month_index = int(callback.data.split('_')[-1])
    kb = await build_days_keyboard(month_index)
    await callback.message.edit_text('Выберите день', reply_markup=kb.as_markup())
