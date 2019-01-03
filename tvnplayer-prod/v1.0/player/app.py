from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify
from flask import make_response
import parse

app = Flask(__name__)
Bootstrap(app)

# show table


@app.route('/')
def mainpage():
    rows = parse.run()
    return render_template('index.html', rows=rows)

# download json


@app.route('/get/<int:serial>')
def get(serial):
    print('getting serial with id {}'.format(serial))
    return 'getting serial with id {}'.format(serial)

# show raw json file


@app.route('/raw/<int:serial>')
def raw(serial):
    print('getting serial with id {}'.format(serial))
    # return jsonify(parse.load_raw(serial))
    response = make_response(parse.load_raw(serial))
    response.headers['Content-Type'] = 'application/json'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0')
