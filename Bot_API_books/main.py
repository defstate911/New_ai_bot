import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для поиска книги по названию
def search_books(query):
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}"
    response = requests.get(url)
    return response.json()

# Функция для получения информации о первой найденной книге
def get_book_info(query):
    data = search_books(query)
    if 'items' in data:
        book = data['items'][0]['volumeInfo']
        title = book.get('title', 'Неизвестно')
        authors = ', '.join(book.get('authors', ['Неизвестные авторы']))
        description = book.get('description', 'Описание отсутствует.')
        image_link = book.get('imageLinks', {}).get('thumbnail', None)
        return title, authors, description, image_link
    return None

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши название книги, и я постараюсь найти её для тебя.")

@dp.message()
async def send_book_info(message: Message):
    query = message.text
    book_info = get_book_info(query)
    if book_info:
        title, authors, description, image_link = book_info
        info = (
            f"Название: {title}\n"
            f"Авторы: {authors}\n"
            f"Описание: {description}"
        )

        # Обрезаем caption, если длина превышает лимит
        max_caption_length = 1024
        if len(info) > max_caption_length:
            info = info[:max_caption_length]  # Обрезаем до 1024 символов

        if image_link:
            await message.answer_photo(photo=image_link, caption=info)
        else:
            await message.answer(info)
    else:
        await message.answer("Книга не найдена. Попробуйте еще раз.")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




