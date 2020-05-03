
from json import dump

from config import DATABASE_DIR, QID_FILENAME
from config import HOSTS_DIR, HOST_FILENAME
from config import TOOLS_FILENAME

from database import read_json


def init_tools_json(host):
    schema = {"ip": host,
              "tanium": 1,
              "qualys": 1,
              "splunk": 1
              }


def save_json(jfile, data):
    pass


def set_tool(host, name, status):

    pass
