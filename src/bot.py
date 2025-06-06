import asyncio

from bot_instance import bot, dp
from config import API_URL, BOT_TOKEN
from core.base_api import BaseAPI
from fallback import fallback_router
from info.handler import info_router
from main_menu.handler import main_menu_router
from middlewares import message_logging, permissions_check
from schedule.handler import schedule_router
from student.handler import student_router
from teacher.handler import teacher_router

dp.include_routers(
    main_menu_router,
    schedule_router,
    student_router,
    # feedback_router,
    teacher_router,
    info_router,
    # -------------------------------
    fallback_router,
)

dp.message.middleware(message_logging.MessageLoggingMiddleware())
dp.message.middleware(permissions_check.GroupLeadMiddleware())


async def main():
    await BaseAPI.init(api_url=API_URL, token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
