from copy import deepcopy

from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart, Text
from database.database import users_db, user_dict_template
from keyboards.bookmarks_kb import create_bookmarks_kb, edit_bookmarks_kb
from keyboards.pagination_kb import create_pagination_kb
from services.file_handing import book
from lexicon.lexicon import LEXICON
from filters.filters import IsDigit, IsBookmark

router: Router = Router()


# START command and ADD user to DB
@router.message(CommandStart())
async def start_command(message: Message) :
    await message.answer(LEXICON['/start'])
    if message.from_user.id not in users_db:
        print(f'{message.from_user.id} added to DB')
        users_db[message.from_user.id] = deepcopy(user_dict_template)


# HELP Command
@router.message(Command(commands='help'))
async def help_command(message: Message):
    await message.answer(LEXICON['/help'])


# BEGINNING command
@router.message(Command(commands='beginning'))
async def begining_command(message: Message):
    users_db[message.from_user.id]['page'] = 1
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
        'backward',
        f"{users_db[message.from_user.id]['page']}/{len(book)}",
        'forward'))


# CONTINUE command
@router.message(Command(commands='continue'))
async def continue_command(message: Message):
    text = book[users_db[message.from_user.id]['page']]
    await message.answer(
        text=text,
        reply_markup=create_pagination_kb(
        'backward',
        f"{users_db[message.from_user.id]['page']}/{len(book)}",
        'forward'))


# BOOKMARKS show command
@router.message(Command(commands='bookmarks'))
async def bookmarks_command(message: Message):
    if users_db[message.from_user.id]['bookmarks']:
        await message.answer(
            text=LEXICON['/bookmarks'],
            reply_markup=create_bookmarks_kb(
            *users_db[message.from_user.id]['bookmarks']))
    else:
        await message.answer(LEXICON['no_bookmarks'])


# FORWARD callback button
@router.callback_query(Text(text='forward'))
async def forward_btn(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] < len(book):
        users_db[callback.from_user.id]['page'] += 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_kb(
                                        'backward',
                                        f"{users_db[callback.from_user.id]['page']}/{len(book)}",
                                        'forward'))

    await callback.answer()


# BACKWARD callback button
@router.callback_query(Text(text='backward'))
async def backward_btn(callback: CallbackQuery):
    if users_db[callback.from_user.id]['page'] > 1:
        users_db[callback.from_user.id]['page'] -= 1
        text = book[users_db[callback.from_user.id]['page']]
        await callback.message.edit_text(text=text,
                                         reply_markup=create_pagination_kb(
                                         'backward',
                                         f"{users_db[callback.from_user.id]['page']}/{len(book)}",
                                         'forward'))

    await callback.answer()


# BOOKMARKS add
@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def bookmark_btn(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].add(
        users_db[callback.from_user.id]['page'])
    await callback.answer('Страница добавлена в закладки')


# BOOKMARKS open
@router.callback_query(IsDigit())
async def bookmark_open_btn(callback: CallbackQuery):
    text = book[int(callback.data)]
    users_db[callback.from_user.id]['page'] = int(callback.data)
    await callback.message.edit_text(text=text,
                                     reply_markup=create_pagination_kb(
                                     'backward',
                                     f"{users_db[callback.from_user.id]['page']}/{len(book)}",
                                     'forward'))

    await callback.answer()


# BOOKMARKS edit
@router.callback_query(Text(text='edit_bookmarks'))
async def bookmarks_edit_btn(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                     reply_markup=edit_bookmarks_kb(
                                     *users_db[callback.from_user.id]['bookmarks']))

    await callback.answer()


# BOOKMARKS cancel edit
@router.callback_query(Text(text='cancel'))
async def bookmarks_cancel_edit(callback: CallbackQuery):
    await callback.message.edit_text(text=f"{LEXICON['cancel_edit']} - {LEXICON['cancel_text']}")
    await callback.answer()


# BOOKMARKS deleting
@router.callback_query(IsBookmark())
async def bookmark_del_btn(callback: CallbackQuery):
    users_db[callback.from_user.id]['bookmarks'].remove(int(callback.data[:-3]))

    if users_db[callback.from_user.id]['bookmarks']:
        await callback.message.edit_text(text=LEXICON['edit_bookmarks'],
                                        reply_markup=edit_bookmarks_kb(
                                        *users_db[callback.from_user.id]['bookmarks']))
    else:
        await callback.message.edit_text(text=LEXICON['no_bookmarks'])
    await callback.answer()