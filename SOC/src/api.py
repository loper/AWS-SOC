
from json import dump

from config import DATABASE_DIR, QID_FILENAME
from config import HOSTS_DIR, HOST_FILENAME
from config import TOOLS_FILENAME, DEFAULT_TOOLS_STATUS

from database import read_json


def init_tools_json(host):
    schema = {"ip": host,
              "tanium": DEFAULT_TOOLS_STATUS,
              "qualys": DEFAULT_TOOLS_STATUS,
              }
    # find TOOLS_FILENAME in tree
    # save new json file with the schema
    pass


def save_json(jfile, data):
    pass


def set_tool(host, name, status):
    # find TOOLS_FILENAME in tree
    # load file - if not exists, create from init_tools_json()
    # set status to 1/0 of key
    # save json
    pass


def set_qid(host, qid=None):
    # find TOOLS_FILENAME in tree
    # load file - if not exists, create from init_tools_json()
    # if qid is None, remove from file that key
    # replace value if already set
    pass


def clear_qid(host):
    # remove 'qid' key from json
    pass


def clear_tools(host):
    # remove all tools keys from json
    pass
