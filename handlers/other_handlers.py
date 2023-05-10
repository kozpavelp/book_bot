from aiogram import Router
from aiogram.types import Message


router: Router = Router()


# Ответ на любые другие сообщения
@router.message()
async def wrong_text(message: Message):
    await message.answer(text='жмите кнопки')
