from aiogram import Router, types

fallback_router = Router()

@fallback_router.message()
def fallback_meesage(message: types.Message):
    pass
