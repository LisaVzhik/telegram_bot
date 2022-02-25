from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

button0 = KeyboardButton('/start')
button1 = KeyboardButton('/plan')
button2 = KeyboardButton('/help')
button4 = KeyboardButton('/all_tasks')
button5 = KeyboardButton('/google_calendar')
kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button0, button2, button1, button4, button5)


def setting_tasks():
    """ Клавиатура для настройки задачи """
    keyboard = [[InlineKeyboardButton("Удалить", callback_data="delete"),
                 InlineKeyboardButton("Изменить дату", callback_data="set date")]]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def tasks(task):
    """ Клавиатура с номерами задач """
    keyboard = []
    row = []
    for n in range(len(task)):
        row.append(InlineKeyboardButton(f"{n+1}", callback_data=f"{n+1}button"))
    keyboard.append(row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

