
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton

from utils.api.user import StudentAPI

async def build_main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='👤 Профиль / Настройки'))
    kb.add(KeyboardButton(text='📅 Расписание'))
    kb.add(KeyboardButton(text='🔍 Найти преподавателя'))
    kb.add(KeyboardButton(text='📚 Домашнее задание'))
    kb.add(KeyboardButton(text='➕ Другое'))
    kb.adjust(1, 2, 2)

    return kb


async def build_other_main_keyboard(user_id: int, group_id: int):
    lead = await StudentAPI.check_group_leadership(user_id=user_id, group_id=group_id)
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text='📝 Документы'))
    kb.add(KeyboardButton(text='💸 Оплата общежития'))
    kb.add(KeyboardButton(text='❓ F.A.Q.'))
    if lead:
        kb.add(KeyboardButton(text='🛠 Управление группой'))
    kb.add(KeyboardButton(text='◀️ Назад'))
    kb.adjust(2, 1, 1)

    return kb
