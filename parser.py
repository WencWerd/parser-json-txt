import json
import sys
import requests
import os
import datetime
import pathlib

today = datetime.datetime.today()
today = (today.strftime("%d.%m.%Y %H:%M"))

try:
    file_users = requests.get("https://json.medrating.org/users")
    file_users = json.loads(file_users.text)
    file_todo = requests.get("https://json.medrating.org/todos")
    file_todo = json.loads(file_todo.text)
except Exception:
    print('Проблемы с сетью')
    sys.exit()


def line_length(): # Функция подсчета символов в строке задания
    try:
        if len(task['title']) <= 48:
            title = f'{task["title"]} \n'
        else:
            title = f'{task["title"][:48]}...\n'
        return title
    except KeyError:
         e = sys.exc_info()[1]
         print(f'Отсутствует "{e.args[0]}"')


def writing_to_file(): # Функция для создания директории и записи в файл
    pathlib.Path('tasks/').mkdir(parents=True, exist_ok=True)
    try:
        f = open(f'tasks/{staff["username"]}.txt', 'x', encoding='utf-8')
        f.write(employee_information)
    except FileExistsError:
        username = f'tasks/{staff["username"]}.txt'
        file_creation_timedatetime = os.path.getmtime(username)
        file_creation_timedatetime = datetime.datetime.fromtimestamp(file_creation_timedatetime).strftime(
            '%Y-%m-%dT%H-%M-%S')
        os.rename(f'{username}', f'tasks/old_{staff["username"]}_{file_creation_timedatetime}.txt')
        f = open(f'{username}', 'x', encoding='utf-8')
        f.write(employee_information)


for staff in file_users:
    number_of_tasks = 0
    number_of_completed_tasks = 0
    number_of_remaining_tasks = 0
    completed_tasks = ''
    remaining_tasks = ''

    for task in file_todo:
        try:
            if task['userId'] == staff['id']:
                number_of_tasks += 1
                if task['completed']:
                    number_of_completed_tasks += 1
                    completed_tasks += line_length()
                else:
                    number_of_remaining_tasks += 1
                    remaining_tasks += line_length()
        except KeyError:
            # e = sys.exc_info()[1]
            # print(f'Отсутствует "{e.args[0]}"')
            continue
    try:
        employee_information = f'Отчет для {staff["name"]}.\n' \
                               f'{staff["username"]} <{staff["email"]}> {today}\n' \
                               f'Всего задач: {number_of_tasks}\n\n' \
                               f'Завершённые задачи ({number_of_completed_tasks}):\n{completed_tasks}\n' \
                               f'Оставшиеся задачи ({number_of_remaining_tasks}):\n{remaining_tasks}'
        writing_to_file()
    except KeyError:
        # e = sys.exc_info()[1]
        # print(f'Отсутствует "{e.args[0]}"')
        continue
