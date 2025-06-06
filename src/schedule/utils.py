from datetime import datetime


async def generate_schedule_message(schedule: list[dict], date: datetime):
    if date.strftime("%Y.%m.%d") == datetime.today().strftime("%Y.%m.%d"):
        message = "📅 <b>Ваше расписание на сегодня:</b>\n\n"
        if not schedule:
            message += "Сегодня у вас нет занятий! 🎉 Отдыхайте!\n"
            return message
    else:
        message = f"📅 <b>Ваше расписание на {date.strftime('%d.%m.%Y')}:</b>\n\n"
        if not schedule:
            message += "В этот день у вас нет занятий! 🎉 Отдыхайте!\n"
            return message

    for lesson in schedule:
        message += (
            f"🔸 {lesson.get('time_from')}-{lesson.get('time_to')}\n"
            + f"     📘 <b>Предмет:</b> {lesson.get('name').replace('\n', '')}\n"
            + (
                f"     🚪 <b>Кабинет:</b> {lesson.get('cabinet')}\n"
                if lesson.get("cabinet") != "-1"
                else ""
            )
            + (
                f"     🏫 <b>Корпус:</b> {lesson.get('building')}\n"
                if lesson.get("building") != -1
                else ""
            )
            + (
                f"     👤 <b>Преподаватель:</b> {lesson.get('teacher').get('short_name')}\n"
                if lesson.get("teacher")
                else ""
            )
            + "\n"
        )

    message += "<b>Желаем удачного дня и продуктивных занятий!</b> 🚀"
    return message


async def generate_teacher_schedule_message(
    schedule: list[dict],
    date: datetime,
    teacher: dict[str, str | int | None],
):
    if date.strftime("%Y.%m.%d") == datetime.today().strftime("%Y.%m.%d"):
        message = f"📅 <b>Расписание преподавателя {teacher.get('short_name')} на сегодня</b>\n\n"
        if not schedule:
            message += (
                f"Сегодня у преподавателя {teacher.get('short_name')} нет занятий\n"
            )
            return message
    else:
        message = f"📅 <b>Расписание преподавателя {teacher.get('short_name')} на {date.strftime('%d.%m.%Y')}</b>\n\n"
        if not schedule:
            message += (
                f"В этот день у преподавателя {teacher.get('short_name')} нет занятий\n"
            )
            return message

    for lesson in schedule:
        message += (
            f"🔸 {lesson.get('time_from')}-{lesson.get('time_to')}\n"
            + f"     📘 <b>Предмет:</b> {lesson.get('name').replace('\n', '')}\n"
            + (
                f"     🚪 <b>Кабинет:</b> {lesson.get('cabinet')}\n"
                if lesson.get("cabinet") != -1
                else ""
            )
            + (
                f"     🏫 <b>Корпус:</b> {lesson.get('building')}\n"
                if lesson.get("building") != -1
                else ""
            )
            + "\n"
        )

    return message
