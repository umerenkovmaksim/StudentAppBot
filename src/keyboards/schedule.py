import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from datetime import datetime, timedelta
from keyboards.consts import MONTHS

async def build_date_change_keyboard(date: datetime):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(
        text='⬅️',
        callback_data=f'get_schedule_{(date - timedelta(days=1)).strftime('%Y-%m-%d')}',
    ))
    keyboard.add(InlineKeyboardButton(
        text='🗓️',
        callback_data='schedule_date_choice',
    ))
    keyboard.add(InlineKeyboardButton(
        text='➡️',
        callback_data=f'get_schedule_{(date + timedelta(days=1)).strftime('%Y-%m-%d')}',
    ))

    return keyboard


month_choice_kb = InlineKeyboardBuilder()
for index, month in enumerate(MONTHS):
    month_choice_kb.add(InlineKeyboardButton(
        text=month,
        callback_data=f'schedule_month_set_{index}',
    ))
month_choice_kb.adjust(3, repeat=True)

async def build_days_keyboard(month_index: int):
    kb = InlineKeyboardBuilder()
    year = datetime.now().year
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month_index + 1)
    days = [day for week in days for day in week]

    for day in days:
        kb.add(InlineKeyboardButton(
            text=str(day) if day != 0 else ' ',
            callback_data=f'get_schedule_{datetime(year, month_index + 1, day).strftime("%Y-%m-%d")}' if day != 0 else 'none',
        ))
    kb.adjust(7, repeat=True)
    return kb

