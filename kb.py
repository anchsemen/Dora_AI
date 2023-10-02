from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

menu_1 = [
    [InlineKeyboardButton(text="Мужской", callback_data="man"),
     InlineKeyboardButton(text="Женский", callback_data="woman")],
]

menu_2 = [
    [InlineKeyboardButton(text="Молодой персонаж", callback_data="young"),
     InlineKeyboardButton(text="Взрослый персонаж", callback_data="medium")],
    [InlineKeyboardButton(text="Персонаж средних лет", callback_data="adult")],
]

menu_3 = [
    [InlineKeyboardButton(text="Светлые волосы", callback_data="blond"),
     InlineKeyboardButton(text="Русые волосы", callback_data="lightbrown"),
     InlineKeyboardButton(text="Темные волосы", callback_data="dark")],
]

menu_1 = InlineKeyboardMarkup(inline_keyboard=menu_1)
menu_2 = InlineKeyboardMarkup(inline_keyboard=menu_2)
menu_3 = InlineKeyboardMarkup(inline_keyboard=menu_3)

feed_button = [[InlineKeyboardButton(text='FeedBack для Доры', url='https://forms.gle/uATLoQekFFzLyu9K6')]]
feedback = InlineKeyboardMarkup(inline_keyboard=feed_button)
