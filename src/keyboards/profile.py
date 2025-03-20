from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.api.user import StudentAPI
from utils.api.group import GroupAPI

profile_kb = InlineKeyboardBuilder()
profile_kb.add(InlineKeyboardButton(
    text='Изменить данные',
    callback_data='change_profile_data',
))
# profile_kb.add(InlineKeyboardButton(
#     text='Выйти из аккаунта',
#     callback_data='logout',
# ))

async def build_profile_change_kb(user_id):
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    change_profile_data_kb = InlineKeyboardBuilder()
    first_name, last_name = user.get('first_name'), user.get('last_name')
    group = None
    if group_id := user.get('group_id'):
        resp = await GroupAPI.get_by_id(group_id)
        group = resp.json
    change_profile_data_kb.row(InlineKeyboardButton(
        text=f'  Имя: {first_name or "Не указано"}',
        callback_data='change_first_name',
    ))
    change_profile_data_kb.row(InlineKeyboardButton(
        text=f'  Фамилия: {last_name or "Не указано"}',
        callback_data='change_last_name',
    ))
    # change_profile_data_kb.row(InlineKeyboardButton(
    #     text=f'  Студенческий билет: {student_id or "Не указано"}',
    #     callback_data='change_student_id',
    # ))
    change_profile_data_kb.row(InlineKeyboardButton(
        text=f'  Группа: {group.get("short_name") if group else "Не указано"}',
        callback_data='change_group',
    ))
    # change_profile_data_kb.row(InlineKeyboardButton(
    #     text=f'  Почта: {user.get("email", "Не указано")}',
    #     callback_data='change_email',
    # ))
    change_profile_data_kb.row(InlineKeyboardButton(
        text='◀️Назад',
        callback_data='back_to_profile',
    ))

    return change_profile_data_kb

