from student.api import GroupAPI


async def generate_profile_message(user: dict[str, str | int]):
    first_name, last_name = user.get("first_name"), user.get("last_name")
    group_id = user.get("group_id")
    group = None
    if group_id:
        resp = await GroupAPI.get_by_id(group_id)
        group = resp.json
    return (
        "👤 <i>Ваш профиль:</i>\n\n"
        f"      Имя: <b>{first_name or 'Не указано'}</b>\n"
        f"      Фамилия: <b>{last_name or 'Не указано'}</b>\n"
        f"      Группа: <b>{group.get('short_name') if group else 'Не указана'}</b>\n\n"
        "⚙️ <i>Настройки:</i>\n\n"
        f"      <b>СКОРО ЗДЕСЬ ЧТО-ТО ПОЯВИТСЯ</b>"
    )
