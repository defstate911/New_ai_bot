import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards import get_main_keyboard
from keyboards import get_options_keyboard
from gtts import gTTS
import os
from aiogram.types import Message, FSInputFile
from config import TOKEN
import keyboards as kb

bot = Bot(token=TOKEN)
dp = Dispatcher()

# тестовые примеры
#@dp.message(CommandStart())
#async def start(message: Message):
    #await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.main)
    #await message.answer(f'Приветики, {message.from_user.first_name}', reply_markup=kb.inline_keyboard_test)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f"Приветики, {message.from_user.first_name}!", reply_markup=kb.main)

# Обработчик нажатий на кнопку "Привет"
@dp.message(F.text == "Привет")
async def greet(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

# Обработчик нажатий на кнопку "Пока"
@dp.message(F.text == "Пока")
async def goodbye(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer(f"{message.from_user.first_name}, выбирай ссылку!", reply_markup=kb.inline_keyboard)


@dp.message(Command("dynamic"))
async def dynamic(message: Message):
    keyboard = await kb.get_main_keyboard()
    await message.answer("Нажмите на кнопку ниже:", reply_markup=keyboard)

@dp.callback_query(F.data == "show_more")
async def show_more(callback: CallbackQuery):
    keyboard = await kb.get_options_keyboard()
    await callback.message.edit_text("Выберите опцию:", reply_markup=keyboard)
    await callback.answer()


@dp.callback_query(F.data == "option_1")
async def option_1(callback: CallbackQuery):
    # В будущем здесь можно добавить асинхронные действия, например, запрос к API
    await callback.message.answer("Вы выбрали Опция 1")
    await callback.answer()


@dp.callback_query(F.data == "option_2")
async def option_2(callback: CallbackQuery):
    # В будущем здесь можно добавить асинхронные действия, например, запрос к API
    await callback.message.answer("Вы выбрали Опция 2")
    await callback.answer()

# если под кнопки не нужны ссылки
# @dp.message(Command("dynamic"))
# async def dynamic(message: Message):
#     await message.answer("Нажмите на кнопку ниже:", reply_markup=get_main_keyboard())

# @dp.callback_query(F.data == "show_more")
# async def show_more(callback: CallbackQuery):
#     await callback.message.edit_text("Выберите опцию:", reply_markup=get_options_keyboard())
#     await callback.answer()
#
# @dp.callback_query(F.data == "option_1")
# async def option_1(callback: CallbackQuery):
#     await callback.message.answer("Вы выбрали Опция 1")
#     await callback.answer()
#
# @dp.callback_query(F.data == "option_2")
# async def option_2(callback: CallbackQuery):
#     await callback.message.answer("Вы выбрали Опция 2")
#     await callback.answer()


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help\n/links\n/dynamic")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
