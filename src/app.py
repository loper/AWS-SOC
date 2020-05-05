from flask import Flask, render_template, url_for, redirect
from flask import jsonify
from flask_bootstrap import Bootstrap

from database import get_found_qids, get_hosts, get_qids
from resources import run as run_refresh
from api import set_qid, set_tool, clear_tools
from config import HEADER, Q_HEADER

APP = Flask(__name__)
Bootstrap(APP)


@APP.route('/', defaults={'sort': 'name', 'vuln': False})
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


@APP.route('/tool/<host>/<name>/<status>')
def set_host_tool(host, name, status):
    set_tool(host, name, status)
    data = {'code': 200, 'status': "Value set"}
    return jsonify(data)


@APP.route('/tool/<host>/reset')
def reset_host_tools(host):
    clear_tools(host)
    data = {'code': 200, 'status': "Value reseted"}
    return jsonify(data)


@APP.route('/qid/<host>/<qid>')
def set_host_qid(host, qid):
    set_qid(host, qid)
    data = {'code': 200, 'status': "Value set"}
    return jsonify(data)


@APP.route('/qid/<host>/reset')
def reset_host_qid(host):
    set_qid(host)
    data = {'code': 200, 'status': "Value reseted"}
    return jsonify(data)


if __name__ == "__main__":
    APP.add_url_rule('/favicon.ico',
                     redirect_to=url_for('static', filename='favicon.ico'))
    APP.run(host='0.0.0.0')
