import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, WEATHER_API_KEY
import sqlite3
import aiohttp
import logging

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты класса?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state:FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

# Формируем сообщение с информацией
    response_message = (
        f"Спасибо! Я записал следующую информацию:\n"
        f"Имя: {user_data['name']}\n"
        f"Возраст: {user_data['age']}\n"
        f"Класс: {user_data['grade']}\n"
        f"Данные успешно сохранены!"
    )
    # Отправляем сообщение пользователю
    await message.answer(response_message)

    # Сбрасываем состояние FSM
    await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())