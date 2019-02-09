""" download methods """

from urllib.request import urlretrieve
from os import remove
from os.path import getmtime, isfile, exists
from os import makedirs
from time import sleep

import config

def get_size(result):
    return int(result.get_all('Content-Length')[0])

def retrieve(serial):
    """ download json from player's api """
    check_dir(config.JSON_DIR)
    link_url = "{}{}".format(config.PLAYER_URL, serial)
    dest = "{}/{}.json".format(config.JSON_DIR, serial)

    if isfile(dest):
        return 'ALREADY DOWNLOADED'

    result = urlretrieve(link_url, dest)
    print('[DEBUG] Downloading data {} - {}'.format(result[0], result[1]))
    try:
        file_size = get_size(result[1])
        assert file_size > 1000
    except:
        remove(dest)
        return 'INVALID FILE'
    return str(result[1])

def get_image(url, dest):
    result = urlretrieve(url, dest)
    print('[DEBUG] Downloading image {} - {}'.format(result[0], result[1]))
    # TODO: https://stackoverflow.com/questions/21746750/check-and-wait-until-a-file-exists-to-read-it
    sleep(1)
    return isfile(dest)

def check_dir(directory):
    if not exists(directory):
        makedirs(directory)
