AAP_NAME = 'AWS SOC'
APP_VERSION = '1.0.0'

DATA_DIR = '/data'
HOSTS_DIR = '{}/hosts'.format(DATA_DIR)
DATABASE_DIR = '{}/database'.format(DATA_DIR)
HOST_FILENAME = 'host.json'
QID_FILENAME = 'qid.json'
TOOLS_FILENAME = 'tools.json'
TOOLS_LIST = ['tanium', 'qualys', 'splunk']

TOOLS_COUNT = 3
DEFAULT_TOOLS_STATUS = 'N/A'


HEADER = ["status", "name", "ip", "os", "tanium", "qualys", "splunk", "qid", "last check"]
Q_HEADER = ["host", "qid", "description", "solution"]
