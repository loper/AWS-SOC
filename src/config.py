AAP_NAME = 'AWS SOC'
APP_VERSION = '0.0.1'

DATA_DIR = '/home/msy/Projekty/SOC/data'
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
