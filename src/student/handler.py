import logging
from http import HTTPStatus

from aiogram import F, Router, filters, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_instance import bot
from main_menu.keyboard import build_main_keyboard
from schedule.consts import INDEX_INSTITUTE
from schedule.keyboard import (
    build_degree_keyboard,
    build_group_keyboard,
    build_institute_keyboard,
)
from student.api import GroupAPI, StudentAPI
from student.keyboard import build_profile_change_kb, profile_kb
from student.utils import generate_profile_message

student_router = Router()


@student_router.message(filters.Command("connect"))
async def connect_group(message: types.Message):
    user_id = message.from_user.id
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.get("json")
    if user and (group_id := user.get("group_id")):
        lead_check = await StudentAPI.check_group_leadership(
            user_id=user.get("id"),
            group_id=group_id,
        )
        if lead_check:
            status_code = await GroupAPI.patch(
                group_id=group_id,
                chat_id=message.chat.id,
            )
            if status_code == HTTPStatus.NO_CONTENT:
                await message.reply("Чат группы был успешно подключен")
                return
    await message.reply(
        "Для подключения чата к боту требуется ввод команды от аккаунта старосты группы",
    )


@student_router.callback_query(F.data == "create_profile")
async def create_profile(callback: types.CallbackQuery):
    kb = await build_institute_keyboard()
    await callback.message.edit_text(
        "Давай начнем. Для начала выбери институт",
        reply_markup=kb.as_markup(),
    )


@student_router.callback_query(F.data == "change_group")
async def change_group(callback: types.CallbackQuery):
    kb = await build_institute_keyboard(profile=True)
    await callback.message.edit_text(
        "Давай начнем. Для начала выбери институт",
        reply_markup=kb.as_markup(),
    )


@student_router.callback_query(F.data.startswith("set_institute"))
async def set_user_institute(callback: types.CallbackQuery):
    institute = INDEX_INSTITUTE[int(callback.data.split("_")[-1])]
    keyboard = await build_degree_keyboard(institute=institute)
    await callback.message.edit_text(
        "Отлично! Теперь выбери курс",
        reply_markup=keyboard.as_markup(),
    )


@student_router.callback_query(F.data.startswith("set_degree"))
async def set_user_degree(callback: types.CallbackQuery):
    degree = int(callback.data.split("_")[-1])
    institute = INDEX_INSTITUTE[int(callback.data.split("_")[-2])]
    keyboard = await build_group_keyboard(
        institute=institute,
        degree=degree,
    )
    await callback.message.edit_text(
        "Отлично! Теперь выбери групп",
        reply_markup=keyboard.as_markup(),
    )


@student_router.callback_query(F.data.startswith("set_group"))
async def set_user_group(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    group_id = int(callback.data.split("_")[-1])
    resp = await GroupAPI.get_by_id(group_id)
    group = resp.json
    resp = await StudentAPI.post(
        json_data={"telegram_id": user_id, "group_id": group_id},
    )
    if resp.status == HTTPStatus.CREATED:
        kb = await build_main_keyboard()
        await callback.message.delete()
        await bot.send_message(
            chat_id=user_id,
            text=(
                "🎉 <b>Аккаунт успешно создан!</b>\n"
                "📚 Вы можете изменить все данные об аккаунте, включая курс и группу, в вашем профиле.\n\n"
                + (
                    "📌 <b>Важно!</b> Для полного доступа к функционалу, староста должен подключить группу к этому боту. (если вы являеетесь им, то напишите сюда @test)"
                    "Если он еще не сделал это, пожалуйста, напомните ему об этом. Бот предоставляет множество функций, "
                    "которые значительно облегчат учебный процесс для студентов!\n"
                    ""
                    if group
                    and not group.get("chat_id")
                    or not group.get("group_leader_id")
                    else ""
                )
            ),
            reply_markup=kb.as_markup(resize_keyboard=True),
        )
    else:
        logging.error(resp.json)
        await callback.message.edit_text("Произошла ошибка, попробуйте еще раз")


class StudentData(StatesGroup):
    first_name = State()
    last_name = State()
    student_id = State()


@student_router.message(F.text == "👤 Профиль / Настройки")
async def profile_handler(message: types.Message):
    user_id = message.from_user.id
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    message_text = await generate_profile_message(user)

    await message.answer(
        message_text,
        reply_markup=profile_kb.as_markup(),
    )


@student_router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    message_text = await generate_profile_message(user)

    await callback.message.edit_text(
        message_text,
        reply_markup=profile_kb.as_markup(),
    )


@student_router.callback_query(F.data == "logout")
async def logout(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    if user:
        is_updated = await StudentAPI.patch(user.get("id"), telegram_id=None)
        if is_updated:
            await callback.message.edit_text(
                text="Вы успешно вышли из аккаунта!",
            )
            return
    await bot.send_message(
        user_id,
        text="Произошла ошибка, попробуйте еще раз",
    )


@student_router.callback_query(F.data == "change_profile_data")
async def change_profile_data(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    kb = await build_profile_change_kb(user_id=user_id)
    await callback.message.edit_text(
        text="Нажмите на кнопку, для того чтобы изменить данные",
        reply_markup=kb.as_markup(),
    )


@student_router.callback_query(F.data.startswith("profile_set_institute"))
async def change_institute(callback: types.CallbackQuery):
    institute = INDEX_INSTITUTE[int(callback.data.split("_")[-1])]
    kb = await build_degree_keyboard(institute=institute, profile=True)
    await callback.message.edit_text(
        "Выберите ваш курс",
        reply_markup=kb.as_markup(),
    )


@student_router.callback_query(F.data.startswith("profile_set_degree"))
async def change_degree(callback: types.CallbackQuery):
    degree = int(callback.data.split("_")[-1])
    institute = INDEX_INSTITUTE[int(callback.data.split("_")[-2])]
    keyboard = await build_group_keyboard(
        institute=institute,
        degree=degree,
        profile=True,
    )
    await callback.message.edit_text(
        text="Выберите группу",
        reply_markup=keyboard.as_markup(),
    )


@student_router.callback_query(F.data.startswith("profile_set_group"))
async def set_profile_user_group(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    group_id = int(callback.data.split("_")[-1])
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    updated_user = await StudentAPI.patch(user.get("id"), group_id=group_id)
    if updated_user.ok:
        kb = await build_profile_change_kb(user_id)
        await callback.message.edit_text(
            "Ваша группа была обновлена",
            reply_markup=kb.as_markup(),
        )
    else:
        await callback.message.edit_text("Произошла ошибка, попробуйте еще раз")


@student_router.callback_query(F.data == "change_first_name")
async def change_first_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите ваше имя")
    await state.set_state(StudentData.first_name)


@student_router.message(StudentData.first_name)
async def set_first_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.text
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    is_updated = await StudentAPI.patch(user.get("id"), first_name=first_name)
    if is_updated.ok:
        kb = await build_profile_change_kb(user_id=user_id)
        await bot.send_message(
            user_id,
            "Имя было успешно изменено",
            reply_markup=kb.as_markup(),
        )

    else:
        await bot.send_message(
            user_id,
            "Произошла ошибка, попробуйте еще раз",
        )
    await state.clear()


@student_router.callback_query(F.data == "change_last_name")
async def change_last_name(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Введите вашу фамилию")
    await state.set_state(StudentData.last_name)


@student_router.message(StudentData.last_name)
async def set_last_name(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    last_name = message.text
    resp = await StudentAPI.get(telegram_id=user_id)
    user = resp.json[0]
    is_updated = await StudentAPI.patch(user.get("id"), last_name=last_name)
    if is_updated.ok:
        kb = await build_profile_change_kb(user_id=user_id)
        await bot.send_message(
            user_id,
            "Фамилия была успешно изменена",
            reply_markup=kb.as_markup(),
        )
    else:
        await bot.send_message(
            user_id,
            "Произошла ошибка, попробуйте еще раз",
        )
    await state.clear()
