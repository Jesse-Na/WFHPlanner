from flask import Flask, render_template, request, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def submit_task():
    if request.method == 'POST':
        print(request.form['email'])
        return render_template("index.html")
    else:
        return render_template("index.html")
