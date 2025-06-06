from aiogram import F, Router, types
from aiogram.filters import CommandStart

from bot_instance import ParseMode
from main_menu.keyboard import build_main_keyboard, build_other_keyboard, start_keyboard
from student.api import StudentAPI

main_menu_router = Router()


@main_menu_router.message(CommandStart(), flags={"auth_handler": True})
async def start(message: types.Message):
    user_id = message.from_user.id
    user = await StudentAPI.get(telegram_id=user_id)
    if user.json:
        kb = await build_main_keyboard()
        await message.answer(
            f"С возвращением, <b>{message.from_user.first_name or message.from_user.username}</b>!",
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
    else:
        text = (
            f"Привет, <b>{message.from_user.first_name or message.from_user.username}</b>!\n\n"
            "Это бот для студентов *Тимирязевской Академии* 🎓\n\n"
            "Здесь ты можешь:\n"
            "• Смотреть расписание\n"
            "• Записывать домашнее задание и делиться им с одногруппниками\n"
            "• Узнавать о важных новостях твоей группы и вуза\n\n"
            "И многое другое\n\nЧтобы начать пользоваться ботом, нажми кнопку ниже"
        )

        await message.answer(
            text=text,
            reply_markup=start_keyboard.as_markup(),
        )


@main_menu_router.message(F.text == "➕ Другое")
async def other_kb(message: types.Message):
    kb = await build_other_keyboard(message.from_user.id)
    await message.answer(
        text="Для возвращения в главное меню, нажмите кнопку `◀️ Назад`",
        reply_markup=kb.as_markup(resize_keyboard=True),
        parse_mode=ParseMode.MARKDOWN,
    )


@main_menu_router.message(F.text == "◀️ Назад")
async def main_kb(message: types.Message):
    kb = await build_main_keyboard()
    await message.answer(
        text="Вы вернулись в главное меню",
        reply_markup=kb.as_markup(resize_keyboard=True),
    )
