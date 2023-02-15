from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup


def text() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Yes', callback_data='image')],
        [InlineKeyboardButton('No', callback_data='finish')],
        [InlineKeyboardButton('Change text', callback_data='new_text')]
    ])
    return kb


def image() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Show me', callback_data='finish_')],
        [InlineKeyboardButton('Change image', callback_data='new_image')]
    ])
    return kb


def finish() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Send to groups', callback_data='send')],
        [InlineKeyboardButton('Cancel operation', callback_data='cancel')]
    ])
    return kb


def finish_() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Send to groups', callback_data='send_')],
        [InlineKeyboardButton('Cancel operation', callback_data='cancel')]
    ])
    return kb
