import re

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from keyboards.consts import INSTITUTE_INDEX
from utils.api.group import GroupAPI, InstituteAPI


login_keyboard = InlineKeyboardBuilder()
login_keyboard.add(InlineKeyboardButton(
    text='Войти',
    callback_data='auth',
))
login_keyboard.adjust(1, 1)

start_keyboard = InlineKeyboardBuilder()
start_keyboard.add(InlineKeyboardButton(
    text='Начать',
    callback_data='create_profile',
))
start_keyboard.adjust(1, 1)

async def build_institute_keyboard(profile=False):
    institute_keyboard = InlineKeyboardBuilder()
    resp = await InstituteAPI.get()
    data = resp.json
    for institute in data:
        institute_name = re.sub(r'институт|Институт', '', institute).strip()
        institute_name = institute_name[0].upper() + institute_name[1:]
        institute_keyboard.row(InlineKeyboardButton(
            text=institute_name,
            callback_data=f'{"profile_" if profile else ""}set_institute_{INSTITUTE_INDEX[institute]}',
        ))

    return institute_keyboard

async def build_degree_keyboard(institute, profile=False):
    degree_keyboard = InlineKeyboardBuilder()
    resp = await GroupAPI.get_degrees(institute=institute)
    data = resp.json
    for degree in data:
        degree_keyboard.row(InlineKeyboardButton(
            text=f"{degree} курс",
            callback_data=f'{"profile_" if profile else ""}set_degree_{INSTITUTE_INDEX[institute]}_{degree}',
        ))

    return degree_keyboard


async def build_group_keyboard(institute, degree, profile=False):
    group_keyboard = InlineKeyboardBuilder()
    resp = await GroupAPI.get(degree=degree, institute=institute)
    data = resp.json
    for group in sorted(data, key=lambda elem: elem['short_name']):
        group_keyboard.add(InlineKeyboardButton(
            text=group.get('short_name'),
            callback_data=f'{"profile_" if profile else ""}set_group_{group['id']}',
        ))

    group_keyboard.adjust(3)

    return group_keyboard
