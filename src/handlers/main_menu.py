from aiogram import Router, types
from aiogram.filters import CommandStart

from utils.api.user import StudentAPI
from keyboards import main_menu, user_settings


router = Router()

@router.message(CommandStart(), flags={'auth_handler': True})
async def start(message: types.Message):
    user_id = message.from_user.id
    user = await StudentAPI.get(telegram_id=user_id)

    if user:
        kb = await main_menu.build_main_keyboard()
        await message.answer(
            f'С возвращением, <b>{message.from_user.first_name or message.from_user.username}</b>!',
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
    else:
        text = (
            f'Привет, <b>{message.from_user.first_name or message.from_user.username}</b>!\n\n'
            'Это бот для студентов *Тимирязевской Академии* 🎓\n\n'
            'Здесь ты можешь:\n'
            '• Смотреть расписание\n'
            '• Записывать домашнее задание и делиться им с одногруппниками\n'
            '• Узнавать о важных новостях твоей группы и вуза\n\n'
            'И многое другое\n\nЧтобы начать пользоваться ботом, нажми кнопку ниже'
        )

        await message.answer(
            text=text,
            reply_markup=user_settings.start_keyboard.as_markup(),
        )
