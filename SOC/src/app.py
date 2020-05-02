from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap

from database import get_found_qids, get_hosts, get_qids
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


if __name__ == "__main__":
    APP.add_url_rule('/favicon.ico',
                     redirect_to=url_for('static', filename='favicon.ico'))
    APP.run(host='0.0.0.0')
