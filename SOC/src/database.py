from json import dump, load, JSONDecodeError

from config import DATABASE_DIR, QID_FILENAME
from config import HOSTS_DIR, HOST_FILENAME
from config import TOOLS_FILENAME

from pathlib import Path

import faker
from _datetime import datetime
from numpy.random import choice
from operator import itemgetter
from os.path import exists


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


def find_tools(host):
    tool_file = '{}/{}/{}'.format(HOSTS_DIR, host, TOOLS_FILENAME)
    if exists(tool_file):
        return tool_file
    return None


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
    if 'N/A' in tools_statuses:
        return 'na'
    if not True in tools_statuses:
        return 'error'
    if False in tools_statuses:
        return 'danger'
    return 'ok'


def add_fake_data(data):
    f = faker.Faker(['en'])
    if not 'tanium' in data:
        data['tanium'] = choice([True, False], p=[0.9, 0.1])
        data['qualys'] = choice([True, False], p=[0.9, 0.1])
        data['splunk'] = choice([True, False], p=[0.8, 0.2])

        data['name'] = f.sentence()
        if [data['tanium'], data['qualys'], data['splunk']].count(False) > 0:
            data['qid'] = choice([372508, 91622, 100403, 99999])

        if [data['tanium'], data['qualys'], data['splunk']].count(False) == 2:
            data['tanium'] = False
            data['qualys'] = False
            data['splunk'] = False
    if not 'last check' in data:
        data['last check'] = datetime.strftime(
            f.date_time_this_year(), '%Y-%m-%d %H:%M:%S')


def set_qid(data):
    # fix missing data
    if not 'qid' in data:
        data['qid'] = 0
    # clear out if all valid
    elif [data['tanium'], data['qualys'], data['splunk']].count(False) == 0:
        data['qid'] = 0


def sort_by(data, attr):
    try:
        rev = False
        if attr == 'qid':
            rev = True
        if not data:
            # empty set
            return data
        if not attr in data[0].keys():
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
        # check tools data
        tools_found = check_tools(data)
        if not tools_found:
            # skip - tools status not found
        #    continue
            data['tanium'] = 'N/A'
            data['qualys'] = 'N/A'
            data['splunk'] = 'N/A'
        # set overall status
        data['status'] = get_status(
            [data['tanium'], data['qualys'], data['splunk']])
        # filter out
        if only_vuln and data['status'] == 'ok':
            continue
        # find QID for host
        set_qid(data)
        # fake data
        add_fake_data(data)  # DEBUG XXX
        result.append(data)

    # sort
    result = sort_by(result, sort_attr)
    return result


def check_tools(host):
    # find json
    tools = find_tools(host['ip'])
    if not tools:
        return False
    # get tools info
    data = read_json(tools)
    # verify file
    if not 'ip' in data.keys() or data['ip'] != host['ip']:
        return False
    # set data from tools status
    set_sec_tools_status(host, data)
    return True


def set_sec_tools_status(host_data, t):
    if 'tanium' in t:
        host_data['tanium'] = t['tanium']
    if 'qualys' in t:
        host_data['qualys'] = t['qualys']
    if 'splunk' in t:
        host_data['splunk'] = t['splunk']
    if 'qid' in t:
        host_data['qid'] = t['qid']


if __name__ == '__main__':
    # print(get_hosts())
    # host details
    hosts_data = get_hosts()

    # QIDs
    qid_list = get_found_qids(hosts_data)
    qids = get_qids(qid_list)
    print(qids)
