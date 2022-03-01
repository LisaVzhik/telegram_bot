import db


def pars_tasks(message):
    """" Нумерованный список текущих задач """
    cmd = message.text
    user_id = message.from_user.id
    if cmd == "/all_tasks":
        tasks = db.list_tasks_date(user_id)
    if cmd == "/plan":
        tasks = db.list_tasks_current_date(user_id)
    list_tasks = [f"{i + 1}. {v}" for i, v in enumerate(tasks)]
    return list_tasks


def google_events(g_events):
    """" Список задач из Google Calendar на текущий день """
    if g_events:
        events_list = [f"{i + 1}. {v}" for i, v in enumerate(g_events)]
        return events_list
    else:
        return "Предстоящие мероприятия не найдены"
