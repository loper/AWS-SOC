from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import parse

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def mainpage():
    rows = parse.run()
    return render_template('index.html', rows=rows)

@app.route('/get/<int:serial>')
def get(serial):
    return 'getting serial with id {}'.format(serial)
