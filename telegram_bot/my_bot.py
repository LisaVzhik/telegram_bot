from aiogram import Bot, types

from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

import asyncio

import config
import keyboards
import db
import parser
import google_api

loop = asyncio.get_event_loop()
bot = Bot(token=config.token)
dp = Dispatcher(bot, loop=loop)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Отправляет приветственное сообщение"""
    if not db.check_user(message.from_user.id):
        db.insert("Users", message.from_user)
    await message.answer(
        f'Привет, {message.from_user.first_name}!\nПросто напиши свои планы.\nПодробнее о моих функциях /help',
        reply_markup=keyboards.kb1)


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    """Отправляет помощь по боту"""
    await message.answer("""
    Команды бота:
    /start --> запускает бота\n 
    /help --> выводит описание команд и функций\n
    /plan --> выводит список задач на текущий день\n
    /all_tasks --> выводит все задачи\n
    /google_calendar --> присылает ссылку для авторизации\n\n
    Функции бота:
    Создать задачу --> написать боту или переслать сообщение(по умолчанию создаются на текущий день)\n
    Изменить дату --> вывести список задач - выбрать номер задачи - выбрать новую дату\n
    Удалить задачу --> вывести список задач - выбрать номер задачи - удалить
    """)


@dp.message_handler(commands=['google_calendar'])
async def cmd_start(message: types.Message):
    """Отправляет ссылку для авторизации"""
    if google_api.auth():
        await message.answer(f"Ссылка для авторизации:\n{google_api.auth()[0]}")


@dp.message_handler(commands=['plan'])
async def cmd_plan(message: types.Message):
    """ Выводит задачи на текущий день """
    plans = parser.pars_tasks(message)
    if plans:
        await message.answer("\n".join(plans),
                             reply_markup=keyboards.tasks(plans), )
    else:
        await message.answer('Задач на сегодня нет :)')


@dp.message_handler(commands=['all_tasks'])
async def cmd_plan(message: types.Message):
    """ Выводит все задачи """
    plans = parser.pars_tasks(message)
    if plans:
        await message.answer("\n".join(plans),
                             reply_markup=keyboards.tasks(plans), )
    else:
        await message.answer('Задач нет :)')


@dp.message_handler(lambda message: message.text)
async def text_handler(message: types.Message):
    """ Создание новой задачи """
    db.insert("Tasks", message)
    await message.answer("Записал")


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    """ Календарь для установки даты """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        db.set_date(date.strftime("%Y-%m-%d"), callback_query.message.chat.id, callback_query.message.text[3:])
        await callback_query.message.answer(
            f'You selected {date.strftime("%Y-%m-%d 00:00:00")}'
        )


@dp.callback_query_handler(lambda c: True)
async def process_callback_button1(callback_query: types.CallbackQuery):
    """ Обработка инлайн кнопок """
    if "button" in callback_query.data:
        selected_task = callback_query.message.text.split("\n")[int(callback_query.data[0]) - 1]
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=selected_task,
                                    reply_markup=keyboards.setting_tasks())

    elif "delete" in callback_query.data:
        task = callback_query.message.text[3:]
        user_id = callback_query.message.chat.id
        db.delete(task, user_id)
        await bot.edit_message_text(chat_id=user_id,
                                    message_id=callback_query.message.message_id,
                                    text="Задача удалена")

    elif "set date" in callback_query.data:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"{callback_query.message.text}",
                                    reply_markup=await SimpleCalendar().start_calendar())


if __name__ == '__main__':
    executor.start_polling(dp)
