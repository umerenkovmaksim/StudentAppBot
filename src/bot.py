import asyncio

from bot_instance import dp, bot
from handlers import schedule, user_settings, fallback, profile, find_teacher, group_lead, main_menu
from middlewares import message_logging, permissions_check
from utils.api.base import BaseAPI
from config import API_URL, BOT_TOKEN


dp.include_routers(
    main_menu.router,
    schedule.schedule_router,
    user_settings.settings_router,
    profile.profile_router,
    # feedback.feedback_router,
    find_teacher.router,
    group_lead.router,
    #-------------------------------
    fallback.fallback_router,
)

dp.message.middleware(message_logging.MessageLoggingMiddleware())
dp.message.middleware(permissions_check.GroupLeadMiddleware())


async def main():
    await BaseAPI.init(api_url=API_URL, token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
