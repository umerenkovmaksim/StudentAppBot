import calendar
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schedule.consts import MONTHS

find_teacher_keyboard = InlineKeyboardBuilder()
find_teacher_keyboard.row(
    InlineKeyboardButton(
        text="Найти по фамилии",
        callback_data="teacher_name",
    ),
)
find_teacher_keyboard.row(
    InlineKeyboardButton(
        text="Список преподавателей",
        callback_data="teacher_list__0",
    ),
)

try_again_name_kb = InlineKeyboardBuilder()
try_again_name_kb.add(
    InlineKeyboardButton(
        text="Попробовать еще раз",
        callback_data="teacher_name",
    ),
)


async def build_teacher_list_kb(teachers, page=0, teacher_filter=""):
    total_pages = (len(teachers) - 1) // 6 + 1
    kb = InlineKeyboardBuilder()
    for teacher in teachers[page * 6 : (page + 1) * 6]:
        kb.row(
            InlineKeyboardButton(
                text=teacher.get("short_name"),
                callback_data=f"get_teacher_schedule_{teacher.get('id')}_{datetime.today().strftime('%Y-%m-%d')}",
            ),
        )

    kb.row(
        InlineKeyboardButton(
            text="⬅️" if page > 0 else " ",
            callback_data=f"teacher_list_{teacher_filter}_{page - 1}"
            if page > 0
            else "none",
        ),
    )
    kb.add(
        InlineKeyboardButton(
            text=f"{page + 1}/{total_pages}",
            callback_data="none",
        ),
    )
    kb.add(
        InlineKeyboardButton(
            text="➡️" if page < total_pages - 1 else " ",
            callback_data=f"teacher_list_{teacher_filter}_{page + 1}"
            if page < total_pages - 1
            else "none",
        ),
    )

    return kb


async def build_date_change_keyboard(date: datetime, teacher_id: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=f"get_teacher_schedule_{teacher_id}_{(date - timedelta(days=1)).strftime('%Y-%m-%d')}",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text="🗓️",
            callback_data=f"teacher_schedule_date_choice_{teacher_id}",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text="➡️",
            callback_data=f"get_teacher_schedule_{teacher_id}_{(date + timedelta(days=1)).strftime('%Y-%m-%d')}",
        ),
    )

    return keyboard


async def build_teacher_schedule_month_keyboard(teacher_id: int):
    kb = InlineKeyboardBuilder()
    for index, month in enumerate(MONTHS):
        kb.add(
            InlineKeyboardButton(
                text=month,
                callback_data=f"teacher_schedule_month_set_{teacher_id}_{index}",
            ),
        )
    kb.adjust(3, repeat=True)
    return kb


async def build_days_keyboard(month_index: int, teacher_id: int):
    kb = InlineKeyboardBuilder()
    year = datetime.now().year
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month_index + 1)
    days = [day for week in days for day in week]
    for day in days:
        kb.add(
            InlineKeyboardButton(
                text=str(day) if day != 0 else " ",
                callback_data=f"get_teacher_schedule_{teacher_id}_{datetime(year, month_index + 1, day).strftime('%Y-%m-%d')}"
                if day != 0
                else "none",
            ),
        )
    kb.adjust(7, repeat=True)
    return kb
