import ast
from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit_task():
    if request.method == 'POST':
        # Time is in 24h format 00:00
        check_in_time = request.form['check_in']
        check_out_time = request.form['check_out']
        task_name = request.form['task_input']
        task_start = request.form['task_start']
        task_end = request.form['task_end']
        task_len = request.form['task_len']
        # task = new Task(task_name, ...)
        tasks = ast.literal_eval(request.form['task_lst']) + [request.form['task_input']]
        return render_template("index.html", tasks=tasks)
    else:
        return render_template("index.html", tasks=[])

