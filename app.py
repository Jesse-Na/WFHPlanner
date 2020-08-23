import os
from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("config.DevelopmentConfig")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Task, add_time


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard', methods=['GET', 'POST'])
def handle_task():
    if request.method == 'POST':
        # Time is in 24h format 00:00
        session['check_in'] = request.form['check_in']
        session['check_out'] = request.form['check_out']
        task_name = request.form['task_input']
        task_start = request.form['task_start']
        task_end = request.form['task_end']
        task_len = request.form['task_len']
        task = Task(task_name, task_start, task_end, task_len)
        db.session.add(task)
        db.session.commit()

    if 'check_in' in session and 'check_out' in session:
        schedule = tasks_to_dicts(organize(session['check_in'], session['check_out'], Task.query.all()))
    else:
        schedule = []

    return render_template("/dashboard.html", tasks=tasks_to_dicts(Task.query.all()), schedule=schedule)

def organize(checkin, checkout, tasks):
    if not tasks:
        return []
    flex_tasks = []
    fixed_tasks = []
    for task in tasks:
        if task.start:
            fixed_tasks.append(task)
        else:
            flex_tasks.append(task)
    fixed_tasks.sort(key=lambda task: to_tuple(task.start))
    flex_tasks.sort(key=lambda task: to_tuple(task.duration))

    ordered_tasks = []
    pointer = checkin
    flex_idx = 0
    fixed_idx = 0
    while flex_idx < len(flex_tasks):
        task = flex_tasks[flex_idx]
        if fixed_idx >= len(fixed_tasks):
            next_fixed = checkout
        else:
            next_fixed = fixed_tasks[fixed_idx].start
        temp = add_time(pointer, task.duration)
        if to_tuple(temp) < to_tuple(next_fixed):
            task.start = pointer
            task.end = temp
            ordered_tasks.append(task)
            flex_idx += 1
            pointer = temp
        else:
            if next_fixed == checkout:
                break
            ordered_tasks.append(fixed_tasks[fixed_idx])
            pointer = fixed_tasks[fixed_idx].end
            fixed_idx += 1
    return ordered_tasks

def to_tuple(time_str):
    return tuple(map(int, time_str.split(':')))

def tasks_to_dicts(tasks):
    return [
        {
            'name': task.name,
            'start': task.start,
            'end': task.end,
        } for task in tasks
    ]



# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         confirm = request.form.get('confirm_password')
#         if not email or not password or password != confirm:
#             return render_template("auth/signup.html")
#         else:
#             return render_template("dashboard.html")
#     else:
#         return render_template("auth/signup.html")
#
# @app.route('/login')
# def login():
#     return render_template("auth/login.html")

if __name__ == '__main__':
    app.run()
