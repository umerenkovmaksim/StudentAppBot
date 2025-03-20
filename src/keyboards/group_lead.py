from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


group_lead_keyboard = InlineKeyboardBuilder()
group_lead_keyboard.add(InlineKeyboardButton(
    text='Создать оповещение',
    callback_data='create_group_notification',
))
group_lead_keyboard.add(InlineKeyboardButton(
    text='Участники',
    callback_data='group_members',
))
