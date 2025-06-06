from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from student.api import StudentAPI

start_keyboard = InlineKeyboardBuilder()
start_keyboard.add(
    InlineKeyboardButton(
        text="Начать",
        callback_data="create_profile",
    ),
)
start_keyboard.adjust(1, 1)


async def build_main_keyboard():
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="👤 Профиль / Настройки"))
    kb.add(KeyboardButton(text="📅 Расписание"))
    kb.add(KeyboardButton(text="📚 Материалы"))
    kb.add(KeyboardButton(text="❓ F.A.Q."))
    kb.add(KeyboardButton(text="➕ Другое"))
    kb.adjust(1, 2, 2)

    return kb


async def build_other_keyboard(user_id: int):
    lead = await StudentAPI.check_group_leadership(user_id=user_id)
    kb = ReplyKeyboardBuilder()
    kb.add(KeyboardButton(text="📝 Документы"))
    kb.add(KeyboardButton(text="💸 Оплата общежития"))
    kb.add(KeyboardButton(text="🔍 Найти преподавателя"))
    if lead:
        kb.add(KeyboardButton(text="🛠 Управление группой"))
    kb.adjust(2, 2)
    kb.row(KeyboardButton(text="◀️ Назад"))

    return kb
