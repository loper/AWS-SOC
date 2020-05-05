from os.path import exists
from json import dump

from config import HOSTS_DIR
from config import TOOLS_FILENAME, TOOLS_LIST

from database import read_json


def init_tools_json(host):
    schema = {"ip": host}
    # find TOOLS_FILENAME in tree
    host_dir = '{}/{}'.format(HOSTS_DIR, host)
    if not exists(host_dir):
        return False
    # save new json file with the schema
    dest = '{}/{}'.format(host_dir, TOOLS_FILENAME)
    _save_json(dest, schema)
    return True


def _save_json(jsonfile, data):
    try:
        with open(jsonfile, 'w') as jfile:
            dump(data, jfile)
    except OSError:
        return False
    return True


def _load_tools(host):
    dest = '{}/{}/{}'.format(HOSTS_DIR, host, TOOLS_FILENAME)
    # load file - if not exists, create from init_tools_json()
    if not exists(dest):
        init_tools_json(host)
    data = read_json(dest)
    return data


def _save_tools(host, data):
    dest = '{}/{}/{}'.format(HOSTS_DIR, host, TOOLS_FILENAME)
    _save_json(dest, data)
    return True


def _to_int(val):
    try:
        return int(val)
    except ValueError:
        return 0


def set_tool(host, name, status):
    # read file
    data = _load_tools(host)
    # set status as 1/0
    if isinstance(status, bool):
        status = 1 if status else 0
    status = _to_int(status)
    data[name] = status
    # save json
    _save_tools(host, data)
    return True


def set_qid(host, qid=None):
    # read file
    data = _load_tools(host)
    if not qid and 'qid' in data.keys():
        # empty qid, remove it
        data.pop('qid')
    else:
        # replace value if already set
        data['qid'] = _to_int(qid)
    # save json
    _save_tools(host, data)
    return True


def clear_tools(host):
    # read file
    data = _load_tools(host)

    for tool in TOOLS_LIST:
        if tool in data.keys():
            data.pop(tool)
    # save json
    _save_tools(host, data)
    return True


if __name__ == '__main__':
    HOST = '172.31.62.157'
    # init_tools_json(HOST)
    # set_tool(HOST, 'qualys', 1)
    # set_qid(HOST)
    # clear_tools(HOST)
    # print(_to_int('a'))
