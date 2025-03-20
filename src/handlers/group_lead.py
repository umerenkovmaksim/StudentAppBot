from aiogram import Router, types, F

from keyboards.group_lead import group_lead_keyboard

router = Router()

@router.message(F.text == '🛠 Управление группой', flags={'group_lead_handler': True})
async def group_lead_panel(message: types.Message):
    await message.answer(
        text='Выберите действие',
        reply_markup=group_lead_keyboard.as_markup(),
    )


@router.message(F.data == 'group_members', flags={'group_lead_handler': True})
async def group_members(message: types.Message):
    pass
