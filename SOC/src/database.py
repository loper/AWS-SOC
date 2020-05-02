from json import dump, load, JSONDecodeError

from config import DATABASE_DIR, QID_FILENAME
from config import HOSTS_DIR, HOST_FILENAME
from pathlib import Path

import faker
from _datetime import datetime
from numpy.random import choice
from operator import itemgetter


def read_json(filename):
    try:
        with open(filename, 'r') as jfile:
            data = load(jfile)
    except OSError:
        return None
    except JSONDecodeError:
        return None
    return data


def find_hosts():
    return Path(HOSTS_DIR).glob('**/{}'.format(HOST_FILENAME))


def get_qids(id_list=None):
    data = read_json('{}/{}'.format(DATABASE_DIR, QID_FILENAME))
    result = []
    for qid in data.keys():
        if not id_list or str(qid) in id_list:
            combinded = data[qid]
            combinded.update({'qid': qid})
            result.append(combinded)
    return result


def get_status(tools_statuses):
    if not True in tools_statuses:
        return 'error'
    if False in tools_statuses:
        return 'danger'
    return 'ok'


def add_fake_data(data):
    f = faker.Faker(['en'])
    data['tanium'] = choice([True, False], p=[0.9, 0.1])
    data['qualys'] = choice([True, False], p=[0.9, 0.1])
    data['splunk'] = choice([True, False], p=[0.8, 0.2])

    data['name'] = f.sentence()

    if [data['tanium'], data['qualys'], data['splunk']].count(False) == 2:
        data['tanium'] = False
        data['qualys'] = False
        data['splunk'] = False

    data['last check'] = datetime.strftime(
        f.date_time_this_year(), '%Y-%m-%d %H:%M:%S')


def set_qid(data):
    # DEBUG XXX
    if [data['tanium'], data['qualys'], data['splunk']].count(False) > 0:
        data['qid'] = choice([372508, 91622, 100403, 99999])
    else:
        data['qid'] = 0


def sort_by(data, attr):
    try:
        rev = False
        if attr == 'qid':
            rev = True
        if attr in data[0].keys():
            data = sorted(data, key=itemgetter(attr), reverse=rev)
        else:
            print('[ERROR] sorting failure: {} not in keys'.format(attr))
            raise KeyError
    except KeyError as err:
        attr = 'name'
        data = sorted(data, key=itemgetter(attr), reverse=rev)
    return data


def get_found_qids(hosts_data):
    result = []
    for host in hosts_data:
        if 'qid' in host.keys() and host['qid'] > 0:
            result.append(str(host['qid']))
    return set(result)


def get_hosts(sort_attr=None, only_vuln=False):
    hosts = find_hosts()
    result = []
    for host in hosts:
        data = read_json(host)
        add_fake_data(data)  # DEBUG XXX
        data['status'] = get_status(
            [data['tanium'], data['qualys'], data['splunk']])
        if only_vuln and data['status'] == 'ok':
            continue
        set_qid(data)
        result.append(data)

    # sort
    result = sort_by(result, sort_attr)
    return result


if __name__ == '__main__':
    # print(get_hosts())
    # host details
    hosts_data = get_hosts()

    # QIDs
    qid_list = get_found_qids(hosts_data)
    qids = get_qids(qid_list)
    print(qids)
