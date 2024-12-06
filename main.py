import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import BotCommand, Message, FSInputFile, ContentType
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
from config import TOKEN
import random
from gtts import gTTS
import os
from googletrans import Translator

bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

if not os.path.exists("img"):
    os.makedirs("img")

# Команда /save_foto: запрос фото
@dp.message(Command("save_foto"))
async def react_photo_request(message: Message):
    await message.answer("Отправьте мне фото, и я его сохраню.")

# Обработка фото
@dp.message(F.photo)
async def save_photo(message: Message):
    # Список случайных ответов
    responses = ["Ого, какая фотка!", "Непонятно, что это такое", "Не отправляй мне такое больше"]
    rand_response = random.choice(responses)

    # Сохранение фото
    photo = message.photo[-1]  # Выбираем самое большое качество
    file_path = f"img/{photo.file_id}.jpg"
    await bot.download(photo, destination=file_path)

    # Ответ пользователю
    await message.answer(rand_response)
    await message.answer(f"Фото сохранено в: {file_path}")


# await bot.download(message.photo[-1],destination=f'img/{message.photo[-1].file_id}.jpg')

# Определяем состояние для ожидания ввода города
class WeatherState(StatesGroup):
    waiting_for_city = State()

# Функция для получения погоды
def get_weather(city):
    api_key = "b7d03c1c5c46a905a488af89efc4343f"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = round(data['main']['temp'])
        description = data['weather'][0]['description'].capitalize()
        return f"Погода в {city}: {temp}°C, {description}."
    else:
        return "Не удалось получить погоду. Проверьте название города."

# Команда /start
@dp.message(Command('start'))
async def start(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}! Я бот, который знает погоду в любом городе мира, умею сохранять фото, озвучивать сообщения и переводить текст с английского!. Выберите в меню, то что вы хотите сделать.")

# Команда /help
@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer("Я могу:\n/start - приветствие\n/help - помощь\n/weather - узнать погоду\n/save_foto - сохранить фото\n/voice - записать голосовое\n/translate - перевести с английского")

# Команда /weather
@dp.message(Command('weather'))
async def weather_command(message: Message, state: FSMContext):
    await message.answer("Напишите название города, чтобы узнать погоду.")
    await state.set_state(WeatherState.waiting_for_city)

# Обработка ввода города
@dp.message(StateFilter(WeatherState.waiting_for_city))
async def process_city(message: Message, state: FSMContext):
    city = message.text
    weather_info = get_weather(city)
    await message.answer(weather_info)
    await state.clear()


# Временный файл для сохранения озвученного текста
TEMP_FILE = "user_voice.ogg"

# Определение состояний
class VoiceStates(StatesGroup):
    waiting_for_text = State()

# Команда /voice для начала ввода текста
@dp.message(Command("voice"))
async def start_voice(message: Message, state: FSMContext):
    await message.answer("Введите текст, который вы хотите озвучить:")
    await state.set_state(VoiceStates.waiting_for_text)

# Обработчик следующего сообщения для озвучивания текста
@dp.message(VoiceStates.waiting_for_text)
async def generate_voice(message: Message, state: FSMContext):
    user_text = message.text.strip()

    if not user_text:
        await message.answer("Вы ввели пустой текст. Попробуйте еще раз.")
        return

    try:
        # Генерация голосового сообщения
        tts = gTTS(text=user_text, lang="ru")
        tts.save(TEMP_FILE)

        # Отправка голосового сообщения
        voice_message = FSInputFile(TEMP_FILE)
        await message.answer_voice(voice=voice_message)
        print("Голосовое сообщение отправлено!")
    except Exception as e:
        await message.answer(f"Ошибка при генерации или отправке голосового сообщения: {e}")
        print(f"Ошибка: {e}")
    finally:
        # Удаление временного файла
        if os.path.exists(TEMP_FILE):
            os.remove(TEMP_FILE)
            print("Временный файл удален.")
        await state.clear()


# Команда для перевода
@dp.message(Command("translate"))
async def translate_command(message: Message):
    await message.answer("Пожалуйста, введите текст на английском, который хотите перевести на русский:")


# Обработчик введённого текста для перевода
@dp.message()
async def handle_translation(message: Message):
    # Проверяем, что это текст на английском
    text_to_translate = message.text.strip()

    if not text_to_translate:
        await message.answer("Вы не ввели текст. Попробуйте снова.")
        return

    try:
        # Перевод текста с помощью Google Translate
        translated = translator.translate(text_to_translate, src='en', dest='ru')
        translated_text = translated.text
        await message.answer(f"Перевод:\n{translated_text}")
    except Exception as e:
        await message.answer(f"Ошибка при переводе: {e}")
        print(f"Ошибка: {e}")


# Устанавливаем команды для меню
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начать работу с ботом"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="weather", description="Узнать погоду"),
        BotCommand(command="save_foto", description="Сохранить фото"),
        BotCommand(command="voice", description="записать голосовое сообщение"),
        BotCommand(command="translate", description="Перевести текст с английского на русский"),
    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():
    await set_commands(bot)  # Устанавливаем команды в меню
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
