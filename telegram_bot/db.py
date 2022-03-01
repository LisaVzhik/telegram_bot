from mysql.connector import connect, Error

from datetime import datetime

import config


def connect_db():
    """ Подключение к БД """
    try:
        connection = connect(
            host=config.host,
            user=config.user,
            password=config.password,
            database=config.database
        )
        return connection
    except Error as e:
        print(e)


def cursor_db(connection):
    """ Курсор БД """
    cursor = connection.cursor()
    return cursor


def check_user(user_id):
    """ Проверка пользователе в БД"""
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"SELECT * FROM Users WHERE user_id={user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    return True if result else False


def insert(table, data):
    """ Вставка данных в таблицу """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = ""
    if table == "Users":
        query = f"INSERT INTO Users(user_id, user_name) VALUES ({data['id']}, '{data['first_name']} {data['last_name']}');"
    elif table == "Tasks":
        query = f"INSERT INTO Tasks(user_id, task) VALUES((SELECT id FROM Users WHERE user_id={data['chat']['id']}), '{data['text']}');"

    cursor.execute(query)
    conn.commit()


def delete(text, user_id):
    """ Удаление задачи """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"DELETE FROM Tasks WHERE task='{text}' AND user_id=(SELECT id FROM Users WHERE user_id={user_id});"
    cursor.execute(query)
    conn.commit()


def set_date(date, user_id, text):
    """ Установка даты """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"update Tasks set task_date='{date}' where user_id=(SELECT id FROM Users WHERE user_id={user_id}) AND task='{text}';"
    cursor.execute(query)
    conn.commit()


def list_tasks_current_date(user_id):
    """ Список задач на текущий день """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"SELECT task FROM Tasks WHERE user_id=(SELECT id FROM Users WHERE user_id={user_id}) AND task_date='{datetime.now().date()}';"
    cursor.execute(query)
    current_task = [t[0] for t in cursor.fetchall()]
    return current_task


def list_tasks_date(user_id):
    """ Список всех задач """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"SELECT task FROM Tasks WHERE user_id=(SELECT id FROM Users WHERE user_id={user_id});"
    cursor.execute(query)
    list_tasks = [t[0] for t in cursor.fetchall()]
    return list_tasks


def set_google_calendar(user_id):
    """ Пометка в БД о синхронизации """
    conn = connect_db()
    cursor = cursor_db(conn)
    query = f"update Users set google_calendar=1 where user_id={user_id};"
    cursor.execute(query)
    conn.commit()
