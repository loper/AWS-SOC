from flask import Flask, render_template, url_for, redirect
from flask import jsonify
from flask_bootstrap import Bootstrap

from database import get_found_qids, get_hosts, get_qids
from resources import run as run_refresh
from config import HEADER, Q_HEADER

APP = Flask(__name__)
Bootstrap(APP)


@APP.route('/', defaults={'sort': 'name', 'vuln': True})
@APP.route('/sort=<sort>')
@APP.route('/only_vuln=<vuln>')
@APP.route('/sort=<sort>/only_vuln=<vuln>')
def mainpage(sort='name', vuln=False):
    # index

    # host details
    hosts_data = get_hosts(sort, vuln)

    # QIDs
    qid_list = get_found_qids(hosts_data)
    qid_data = get_qids(qid_list, hosts_data)

    # empty set
    if not hosts_data:
        return render_template('empty.html.j2')

    # format html
    return render_template('index.html.j2',
                           headers=HEADER, data=hosts_data,
                           qid_headers=Q_HEADER, qid_data=qid_data)


@APP.route('/refresh')
def refresh_database():
    # database structure import
    status = run_refresh()
    # return redirect(url_for('mainpage'))
    if not status:
        data = {'code': 500, 'status': "Refresh error"}
    else:
        data = {'code': 200, 'status': "Database refreshed"}
    return jsonify(data)


if __name__ == "__main__":
    APP.add_url_rule('/favicon.ico',
                     redirect_to=url_for('static', filename='favicon.ico'))
    APP.run(host='0.0.0.0')
