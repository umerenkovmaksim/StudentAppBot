import logging
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware, types


class MessageLoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Message, dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: dict[str, Any],
    ) -> Any:
        logging.info(f'"{event.text}" from {event.from_user.id}')
        return await handler(event, data)
