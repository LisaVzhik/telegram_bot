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


def events(google_events):
    """" Список текущих задач из Google Calendar """
    if google_events:
        events_list = [event['summary'] for event in google_events]
        return events_list


def update_tasks(events_list, list_tasks):
    """ Возвращает новые задачи из гугл календаря"""
    new_events = [event for event in events_list if event not in list_tasks]
    return new_events


if __name__ == '__main__':
    print()
