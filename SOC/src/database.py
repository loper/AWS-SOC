from json import dump, load, JSONDecodeError
from os import stat
from time import strftime, localtime

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


def get_host_by_qid(qid, hosts_data):
    for host in hosts_data:
        if str(host['qid']) == str(qid):
            return host['ip']
    return 'N/A'


def get_qids2(id_list, hosts_data):
    data = read_json('{}/{}'.format(DATABASE_DIR, QID_FILENAME))
    result = []
    for qid in data.keys():
        if not id_list or str(qid) in id_list:
            combinded = data[qid]
            host = get_host_by_qid(qid, hosts_data)
            combinded.update({'qid': qid, 'host': host})
            result.append(combinded)
    return result

def get_qids(id_list, hosts_data):
    if not id_list:
        return None
    data = read_json('{}/{}'.format(DATABASE_DIR, QID_FILENAME))
    result = []
    for host in hosts_data:
        if host['qid'] == 0:
            continue
        qid = str(host['qid'])
        if qid not in data.keys():
            continue
        combinded = data[qid]
        combinded.update({'qid': qid, 'host': host['ip']})
        result.append(combinded)
    return result


def get_status(tools_statuses):
    # no data found - NEUTRAL
    if 'N/A' in tools_statuses:
        return 'zero'
    # all tools are invalid - FATAL
    elif not True in tools_statuses:
        return 'error'
    # one of tools are invalid - WARNING
    elif False in tools_statuses:
        return 'danger'
    # everything is good - OK
    return 'ok'


def set_qid(data):
    # fix missing data
    if not 'qid' in data:
        data['qid'] = 0
    # clear out if all valid
    # elif [data['tanium'], data['qualys'], data['splunk']].count(False) == 0:
    #   data['qid'] = 0


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
            # no tools data
            data['tanium'] = 'N/A'
            data['qualys'] = 'N/A'
            data['splunk'] = 'N/A'
        # fix QID for host
        set_qid(data)
        # set overall status
        data['status'] = get_status(
            [data['tanium'], data['qualys'], data['splunk'],
             (data['qid'] == 0)])
        # filter out
        if only_vuln and data['status'] == 'ok':
            continue
        result.append(data)

    # sort
    result = sort_by(result, sort_attr)
    return result


def set_last_change_time(host_data, tools_file):
    changed = stat(tools_file).st_mtime
    changed_time = strftime('%Y-%m-%d %H:%M:%S', localtime(changed))
    host_data['last check'] = changed_time


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
    set_last_change_time(host, tools)
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
    qids = get_qids(qid_list, hosts_data)
    print(qids)

    print(get_host_by_qid(91622, hosts_data))
