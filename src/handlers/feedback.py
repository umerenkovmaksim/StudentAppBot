from http import HTTPStatus
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.feedback import feedback_keyboard, build_student_feedbacks_keyboard
from utils.api.user import StudentAPI
from utils.api.feedback import FeedbackAPI

feedback_router = Router()

class FeedbackForm(StatesGroup):
    title = State()
    text = State()

@feedback_router.message(F.text == 'Обратная связь')
async def feedback(message: types.Message):
    await message.answer(
        text='Если вы нашли баг в нашем приложении, у вас есть проблемы с доступом к нему, или вы хотите написать пожелания для бота, то можете написать нам!',
        reply_markup=feedback_keyboard.as_markup(),
    )

@feedback_router.callback_query(F.data == 'create_feedback')
async def create_student_feedback(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text='Введите тему обращения (до 100 символов)',
    )
    await state.set_state(FeedbackForm.title)

@feedback_router.message(FeedbackForm.title)
async def get_feedback_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer(text='Введите текст обращения')
    await state.set_state(FeedbackForm.text)

@feedback_router.message(FeedbackForm.text)
async def send_feedback(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    resp = await StudentAPI.get(telegram_id=telegram_id)
    user = resp.json[0]
    user_id = user.get('id')
    title = await state.get_value('title')
    text = message.text

    resp = await FeedbackAPI.post(json_data={'user_id': user_id, 'title': title, 'text': text})
    if resp.status == HTTPStatus.CREATED:
        await message.answer('Ваше обращение было успешно отправлено')
    else:
        await message.answer('Произошла ошибка, попробуйте еще раз')
    await state.clear()

@feedback_router.callback_query(F.data.startswith('student_feedbacks_'))
async def student_feedbacks(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    resp = await StudentAPI.get(telegram_id=telegram_id)
    user = resp.json[0]
    user_id = user.get('id')
    page = int(callback.data.split('_')[-1])

    resp = await FeedbackAPI.get(user_id=user_id)
    feedbacks = resp.json[0]
    if not feedbacks:
        await callback.message.edit_text('У вас нет обращений')
        return
    kb = await build_student_feedbacks_keyboard(feedbacks=feedbacks, cur_page=page)

    await callback.message.edit_text(
        'Выберите обращение для просмотра полной информации о нём',
        reply_markup=kb.as_markup(),
    )


