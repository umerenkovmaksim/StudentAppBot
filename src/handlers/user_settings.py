
from aiogram import Router, F, types, filters

from http import HTTPStatus

from bot_instance import bot
from keyboards import user_settings, main_menu
from keyboards.consts import INDEX_INSTITUTE
from utils.api.user import StudentAPI
from utils.api.group import GroupAPI

settings_router = Router()

# class AuthForm(StatesGroup):
#     email = State()
#     code = State()

# @settings_router.callback_query(F.data == 'auth', flags={'auth_handler': True})
# async def user_authorization(callback: types.CallbackQuery, state: FSMContext):
#     user_id = callback.from_user.id

#     await bot.send_message(user_id, 'Введите вашу *почту*', parse_mode='Markdown')
#     await state.set_state(AuthForm.email)


# @settings_router.message(AuthForm.email, flags={'auth_handler': True})
# async def auth_by_email(message: types.Message, state: FSMContext):
#     email = message.text
#     user_id = message.from_user.id
#     user = await get_user_by_email(email=email)
#     if user:
#         student_id = user.get('telegram_id')
#         if student_id:
#             await message.answer('Пользователь с такой почтой привязан к другому аккаунту Telegram\nПопробуйте другую почту или напишите в поддержку')
#             await state.clear()
#         else:
#             updated_user = await update_user(id=user.get('id'), telegram_id=user_id)
#             if updated_user:
#                 await message.answer('Вы успешно вошли в аккаунт')
#                 await state.clear()
#         return
#     else:
#         _, status = await create_user(email=email, telegram_id=user_id)
#         if status == 201:
#             await state.update_data(email=email)
#             await message.answer('На вашу почту был выслан код.\nПожалуйста, введите его сюда\n')
#             await state.set_state(AuthForm.code)
#             return
#         elif status == 403:
#             await state.update_data(email=email)
#             await message.answer('Попыток не осталось, попробуйте позже или попробуйте другую почту')
#             await state.clear()
#             return

#     await message.answer('Ошибка при создании аккаунта или входе в него')
#     await state.clear()


# @settings_router.message(AuthForm.code, flags={'auth_handler': True})
# async def confirm_code(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     email = data.get('email')
#     code = message.text
#     user, status = await confirm_create_user(code=code, email=email)
#     if status == 201:
#         kb = await settings.build_degree_keyboard()
#         await message.answer('Аккаунт был успешно создан. Выберите курс', reply_markup=kb.as_markup())
#         await state.clear()
#     elif status == 400:
#         await message.answer(f'Неверный код, осталось попыток: {user['detail'].get('attempts')}')
#     elif status == 403:
#         await message.answer('Попыток не осталось, попробуйте позже или попробуйте другую почту')
#         await state.clear()
#     else:
#         await message.answer('Произошла ошибка, попробуйте еще раз')
#         await state.clear()


@settings_router.message(filters.Command('connect'))
async def connect_group(message: types.Message):
    user_id = message.from_user.id
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.get('json')
    if user and (group_id := user.get('group_id')):
        lead_check = await StudentAPI.check_group_leadership(user_id=user.get('id'), group_id=group_id)
        if lead_check:
            status_code = await GroupAPI.patch(group_id=group_id, chat_id=message.chat.id)
            if status_code == HTTPStatus.NO_CONTENT:
                await message.reply('Чат группы был успешно подключен')
                return
    await message.reply('Для подключения чата к боту требуется ввод команды от аккаунта старосты группы')

@settings_router.callback_query(F.data == 'create_profile')
async def create_profile(callback: types.CallbackQuery):
    kb = await user_settings.build_institute_keyboard()
    await callback.message.edit_text('Давай начнем. Для начала выбери институт', reply_markup=kb.as_markup())

@settings_router.callback_query(F.data.startswith('set_institute'))
async def set_user_institute(callback: types.CallbackQuery):
    institute = INDEX_INSTITUTE[int(callback.data.split('_')[-1])]
    keyboard = await user_settings.build_degree_keyboard(institute=institute)
    await callback.message.edit_text('Отлично! Теперь выбери курс', reply_markup=keyboard.as_markup())

@settings_router.callback_query(F.data.startswith('set_degree'))
async def set_user_degree(callback: types.CallbackQuery):
    degree = int(callback.data.split('_')[-1])
    institute = INDEX_INSTITUTE[int(callback.data.split('_')[-2])]
    keyboard = await user_settings.build_group_keyboard(institute=institute, degree=degree)
    await callback.message.edit_text('Отлично! Теперь выбери группу', reply_markup=keyboard.as_markup())


@settings_router.callback_query(F.data.startswith('set_group'))
async def set_user_group(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    group_id = int(callback.data.split('_')[-1])
    resp = await GroupAPI.get_by_id(group_id)
    group = resp.json
    resp = await StudentAPI.post(telegram_id=user_id, group_id=group_id)
    user = resp.json[0]
    if user:
        kb = await main_menu.build_main_keyboard()
        await callback.message.delete()
        await bot.send_message(
            chat_id=user_id,
            text=(
                '🎉 <b>Аккаунт успешно создан!</b>\n'
                '📚 Вы можете изменить все данные об аккаунте, включая курс и группу, в вашем профиле.\n\n' +
                ('📌 <b>Важно!</b> Для полного доступа к функционалу, староста должен подключить группу к этому боту. (если вы являеетесь им, то напишите сюда @test)'
                'Если он еще не сделал это, пожалуйста, напомните ему об этом. Бот предоставляет множество функций, '
                'которые значительно облегчат учебный процесс для студентов!\n'
                '' if group and not group.get('chat_id') or not group.get('group_leader_id') else '')
            ),
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
    else:
        await callback.message.edit_text('Произошла ошибка, попробуйте еще раз')
