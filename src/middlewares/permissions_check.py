from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, types

from student.api import StudentAPI


class AuthCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [types.Message | types.CallbackQuery, dict[str, Any]],
            Awaitable[Any],
        ],
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ):
        if data["handler"].flags.get("auth_handler"):
            return await handler(event, data)
        user = await StudentAPI.get(telegram_id=event.from_user.id)
        if not user:
            await event.answer(
                "Для того чтобы пользоваться ботом, авторизуйтесь при помощи команды /start",
            )
            return None
        return await handler(event, data)


class GroupLeadMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[
            [types.Message | types.CallbackQuery, dict[str, Any]],
            Awaitable[Any],
        ],
        event: types.Message | types.CallbackQuery,
        data: dict[str, Any],
    ):
        if data["handler"].flags.get("group_lead_handler"):
            user = await StudentAPI.get(telegram_id=event.from_user.id)
            check = await StudentAPI.check_group_leadership(
                user.get("id"),
                user.get("group_id"),
            )
            if check:
                return await handler(event, data)
            return None
        return await handler(event, data)
