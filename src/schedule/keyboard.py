import calendar
import re
from datetime import datetime, timedelta

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from schedule.api import InstituteAPI
from schedule.consts import INSTITUTE_INDEX, MONTHS
from student.api import GroupAPI


async def build_date_change_keyboard(date: datetime):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=f"get_schedule_{(date - timedelta(days=1)).strftime('%Y-%m-%d')}",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text="🗓️",
            callback_data="schedule_date_choice",
        ),
    )
    keyboard.add(
        InlineKeyboardButton(
            text="➡️",
            callback_data=f"get_schedule_{(date + timedelta(days=1)).strftime('%Y-%m-%d')}",
        ),
    )

    return keyboard


month_choice_kb = InlineKeyboardBuilder()
for index, month in enumerate(MONTHS):
    month_choice_kb.add(
        InlineKeyboardButton(
            text=month,
            callback_data=f"schedule_month_set_{index}",
        ),
    )
month_choice_kb.adjust(3, repeat=True)


async def build_days_keyboard(month_index: int):
    kb = InlineKeyboardBuilder()
    year = datetime.now().year
    cal = calendar.Calendar()
    days = cal.monthdayscalendar(year, month_index + 1)
    days = [day for week in days for day in week]

    for day in days:
        kb.add(
            InlineKeyboardButton(
                text=str(day) if day != 0 else " ",
                callback_data=f"get_schedule_{datetime(year, month_index + 1, day).strftime('%Y-%m-%d')}"
                if day != 0
                else "none",
            ),
        )
    kb.adjust(7, repeat=True)
    return kb


async def build_institute_keyboard(profile=False):
    institute_keyboard = InlineKeyboardBuilder()
    resp = await InstituteAPI.get()
    data = resp.json
    for institute in data:
        institute_name = re.sub(r"институт|Институт", "", institute).strip()
        institute_name = institute_name[0].upper() + institute_name[1:]
        institute_keyboard.row(
            InlineKeyboardButton(
                text=institute_name,
                callback_data=f"{'profile_' if profile else ''}set_institute_{INSTITUTE_INDEX[institute]}",
            ),
        )

    return institute_keyboard


async def build_degree_keyboard(institute, profile=False):
    degree_keyboard = InlineKeyboardBuilder()
    resp = await GroupAPI.get_degrees(institute=institute)
    data = resp.json
    for degree in data:
        degree_keyboard.row(
            InlineKeyboardButton(
                text=f"{degree} курс",
                callback_data=f"{'profile_' if profile else ''}set_degree_{INSTITUTE_INDEX[institute]}_{degree}",
            ),
        )

    return degree_keyboard


async def build_group_keyboard(institute, degree, profile=False):
    group_keyboard = InlineKeyboardBuilder()
    resp = await GroupAPI.get(degree=degree, institute=institute)
    data = resp.json
    for group in sorted(data, key=lambda elem: elem["short_name"]):
        group_keyboard.add(
            InlineKeyboardButton(
                text=group.get("short_name"),
                callback_data=f"{'profile_' if profile else ''}set_group_{group['id']}",
            ),
        )

    group_keyboard.adjust(3)

    return group_keyboard
