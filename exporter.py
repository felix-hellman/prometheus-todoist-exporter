import todoist
from datetime import date
from datetime import datetime
import json
import os.path
import cred
from prometheus_client import start_http_server, Counter
import time


def save(state):
    f = open('.state', 'w')
    f.write(json.dumps(state))
    f.close()


def is_today(date_query):
    return datetime.strptime(date_query, '%Y-%m-%d').date() == date.today()


def load():
    if os.path.isfile('.state'):
        f = open('.state', 'r')
        state = json.loads(f.read())
        f.close()
        completed_today = list(filter(lambda x: is_today(x['completed']), state))
        return completed_today
    return []


def report_completed(completed_tasks, reported, counter):
    completed_today = list(filter(lambda x: is_today(x['completed']), completed_tasks))
    not_reported = list(
        filter(lambda x: x['content'] not in list(map(lambda z: z['content'], reported)), completed_today))
    for task in not_reported:
        print("Reporting " + task['content'])
        counter.labels(task['content']).inc()
        task['reported'] = True
        reported.append(task)
    return reported


def report_completed_tasks(api, prometheus_counter):
    api.sync()
    reported = load()
    recurring_tasks = list(filter(lambda x: x['due']['is_recurring'], api.state['items']))
    completed_tasks = api.completed.get_all()['items']

    content_recurring = list(map(lambda x: x['content'], recurring_tasks))
    completed = list(
        map(lambda x: {'content': x['content'], 'completed': x['completed_date'].split('T')[0], 'reported': False},
            completed_tasks))
    completed_recurring = list(filter(lambda x: x['content'] in content_recurring, completed))
    reported = report_completed(completed_recurring, reported, prometheus_counter)
    save(reported)


if __name__ == '__main__':
    api = todoist.TodoistAPI(cred.key)
    start_http_server(8000)
    c = Counter('todoist_recurring_completed', 'Counter of todoist recurring tasks', ['task_name'])
    print("Exporter started!")
    while True:
        report_completed_tasks(api, c)
        time.sleep(5)
