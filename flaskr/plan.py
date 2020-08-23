import ast

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('plan', __name__, url_prefix='/')

# def sortTasksByPrio(tasks):
#     return sorted(tasks, key=lambda x: x.get_prio(), reverse=True)
#
# def plan(start, end, breaks, fixed_tasks, prio_tasks):

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route('/dashboard', methods=('GET', 'POST'))
def submit_task():
    if request.method == 'POST':
        # Time is in 24h format 00:00
        check_in_time = request.form['check_in']
        check_out_time = request.form['check_out']
        lunch_start = request.form['lunch_start']
        lunch_end = request.form['lunch_end']
        task_name = request.form['task_input']
        task_start = request.form['task_start']
        task_end = request.form['task_end']
        task_len = request.form['task_len']
        # task = new Task(task_name, ...)
        tasks = ast.literal_eval(request.form['task_lst']) + [request.form['task_input']]
        print(tasks)
        return render_template("dashboard.html", tasks=tasks)
    else:
        return render_template("dashboard.html", tasks=[])

        return render_template("dashboard.html")