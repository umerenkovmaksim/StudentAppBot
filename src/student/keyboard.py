from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from student.api import GroupAPI, StudentAPI

profile_kb = InlineKeyboardBuilder()
profile_kb.add(
    InlineKeyboardButton(
        text="Изменить данные",
        callback_data="change_profile_data",
    ),
)


async def build_profile_change_kb(user_id):
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    change_profile_data_kb = InlineKeyboardBuilder()
    first_name, last_name = user.get("first_name"), user.get("last_name")
    group = None
    if group_id := user.get("group_id"):
        resp = await GroupAPI.get_by_id(group_id)
        group = resp.json
    change_profile_data_kb.row(
        InlineKeyboardButton(
            text=f"  Имя: {first_name or 'Не указано'}",
            callback_data="change_first_name",
        ),
    )
    change_profile_data_kb.row(
        InlineKeyboardButton(
            text=f"  Фамилия: {last_name or 'Не указано'}",
            callback_data="change_last_name",
        ),
    )

    change_profile_data_kb.row(
        InlineKeyboardButton(
            text=f"  Группа: {group.get('short_name') if group else 'Не указано'}",
            callback_data="change_group",
        ),
    )

    change_profile_data_kb.row(
        InlineKeyboardButton(
            text="◀️Назад",
            callback_data="back_to_profile",
        ),
    )

    return change_profile_data_kb


group_lead_keyboard = InlineKeyboardBuilder()
group_lead_keyboard.add(
    InlineKeyboardButton(
        text="Создать оповещение",
        callback_data="create_group_notification",
    ),
)
group_lead_keyboard.add(
    InlineKeyboardButton(
        text="Участники",
        callback_data="group_members",
    ),
)
