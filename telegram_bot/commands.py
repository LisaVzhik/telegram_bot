import db
import parser


def start(message):
    """ Проверяет запись о пользователе в БД и генерирует приветсвенное сообщение """
    if not db.check_user(message.from_user.id):
        db.insert("Users", message.from_user)

    welcome_message = f'Привет, {message.from_user.first_name}!\nПодробнее о моих функциях /help'
    return welcome_message


def help_message():
    """ Информация по командам и функциям """
    text = """
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
    """
    return text


def plan(message):
    """ Список задач"""
    list_tasks = parser.pars_tasks(message)
    count_button = len(list_tasks)
    if list_tasks:
        return "\n".join(list_tasks), count_button
    else:
        return "Задач на сегодня нет :)", count_button


def create_task(message):
    db.insert("Tasks", message)
    return


def button(callback_query):
    """ Определене выбранной кнопки """
    selected_task = callback_query.message.text.split("\n")[int(callback_query.data[0]) - 1]
    return selected_task


def delete(callback_query):
    """ Удаляет задачу """
    task = callback_query.message.text[3:]
    user_id = callback_query.message.chat.id
    db.delete(task, user_id)
    return
