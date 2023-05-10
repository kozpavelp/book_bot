from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon.lexicon import LEXICON


# Генерация кнопок для страниц книги
def create_pagination_kb(*buttons: str):
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(*[InlineKeyboardButton(
        text=LEXICON[button] if button in LEXICON else button,
        callback_data=button) for button in buttons])

    return kb_builder.as_markup()
