from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar
import asyncio

import config
import commands
import keyboards
import db


loop = asyncio.get_event_loop()
bot = Bot(token=config.token)
dp = Dispatcher(bot, loop=loop)


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    """Отправляет приветственное сообщение"""
    welcome_message = commands.start(message)
    await message.answer(welcome_message, reply_markup=keyboards.commands())


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    """Отправляет помощь по боту"""
    await message.answer(commands.help_message())


@dp.message_handler(commands=['plan', 'all_tasks'])
async def cmd_plan(message: types.Message):
    """ Выводит задачи на текущий день """
    tasks = commands.plan(message)
    await message.answer(tasks[0], reply_markup=keyboards.tasks(tasks[1]))


@dp.message_handler(commands=['google_calendar'])
async def cmd_start(message: types.Message):
    """Отправляет ссылку для авторизации"""
    google_tasks = commands.google_calendar()
    await message.answer(f"Список задач из Google Calendar:\n{google_tasks}")


@dp.message_handler(lambda message: message.text)
async def cmd_new_task(message: types.Message):
    """ Создание новой задачи """
    commands.create_task(message)
    await message.answer("Записал")


@dp.callback_query_handler(simple_cal_callback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    """ Календарь для установки даты """
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        db.set_date(date.strftime("%Y-%m-%d"), callback_query.message.chat.id, callback_query.message.text[3:])
        await callback_query.message.answer(
            f'Дата задачи изменена на {date.strftime("%Y-%m-%d")}'
        )


@dp.callback_query_handler(lambda c: True)
async def process_callback_button1(callback_query: types.CallbackQuery):
    """ Обработка инлайн кнопок """
    if "button" in callback_query.data:
        selected_task = commands.button(callback_query)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=selected_task,
                                    reply_markup=keyboards.setting_tasks())

    elif "delete" in callback_query.data:
        commands.delete(callback_query)
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text="Задача удалена")

    elif "set date" in callback_query.data:
        await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                    message_id=callback_query.message.message_id,
                                    text=f"{callback_query.message.text}",
                                    reply_markup=await SimpleCalendar().start_calendar())


if __name__ == '__main__':
    executor.start_polling(dp)
