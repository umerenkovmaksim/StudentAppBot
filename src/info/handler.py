from aiogram import F, Router, types

info_router = Router()


@info_router.message(F.text == "❓ F.A.Q.")
async def faq(message: types.Message):
    await message.answer(
        text="В будущем здесь будет информация о вузе, боте, а также нейро-помощник",
    )
