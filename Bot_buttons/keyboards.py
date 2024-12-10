from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет"), KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)


inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Новости", url='https://lenta.ru/')],
   [InlineKeyboardButton(text="Музыка", url='https://music.yandex.ru/album/2409566/track/21083708')],
   [InlineKeyboardButton(text="Видео", url='https://www.youtube.com/watch?v=5P6ADakiwcg&ysclid=m4hdacctmg695465558')]
])


inline_keyboard_dynamic = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Показать больше", callback_data="show_more")],
])


async def get_main_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Показать больше", callback_data="show_more")
    keyboard.adjust(1)
    return keyboard.as_markup()


async def get_options_keyboard():
    # Здесь можно будет добавить асинхронную логику, например, загрузку данных.
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Опция 1", callback_data="option_1")
    keyboard.button(text="Опция 2", callback_data="option_2")
    keyboard.adjust(1)
    return keyboard.as_markup()

# если под кнопки не нужны ссылки
# def get_main_keyboard():
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(text="Показать больше", callback_data="show_more")
#     keyboard.adjust(1)
#     return keyboard.as_markup()
#
# def get_options_keyboard():
#     keyboard = InlineKeyboardBuilder()
#     keyboard.button(text="Опция 1", callback_data="option_1")
#     keyboard.button(text="Опция 2", callback_data="option_2")
#     keyboard.adjust(1)
#     return keyboard.as_markup()