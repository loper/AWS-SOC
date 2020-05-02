AAP_NAME = 'AWS SOC'
APP_VERSION = '0.0.1'

DATA_DIR = '/home/msy/Projekty/SOC/data'
HOSTS_DIR = '{}/hosts'.format(DATA_DIR)
DATABASE_DIR = '{}/database'.format(DATA_DIR)
HOST_FILENAME = 'host.json'
QID_FILENAME = 'qid.json'


HEADER = ["status", "name", "ip", "os", "tanium", "qualys", "splunk", "last check", "qid"]
Q_HEADER = ["qid", "description", "solution"]
