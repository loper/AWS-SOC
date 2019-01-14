from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask import jsonify
from flask import make_response
import parse
import download


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
    print('[DEBUG] requested download for @{}@'.format(serial))
    result = download.retrieve(serial)
    return render_template('result.html', data=result)
    # return redirect(url_for('index'))

# show raw json file


@app.route('/raw/<int:serial>')
def raw(serial):
    print('[DEBUG] getting raw json for @{}@'.format(serial))
    response = make_response(parse.load_raw(serial))
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
