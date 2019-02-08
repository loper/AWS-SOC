import json
import glob
import time
from os.path import getmtime, isfile

import config
from download import check_dir, get_image


def run(json_dir=config.JSON_DIR):
    """ find latest jsons and get data from them """
    check_dir(json_dir)
    # find all json files
    files = glob.glob('{}/*.json'.format(json_dir), recursive=True)
    files.sort(key=getmtime, reverse=True)
    result = []
    for filename in files:
        output = get_data(filename, json_dir)
        if output is None or type(output) == tuple:
            if output[0] is None:
                continue
            result.append(output[0])
        else:
            print('[error] Getting data from file {}'.format(filename))
            print(output)
    return result


def load_raw(asset_id, dir=config.JSON_DIR):
    """ load json file """
    check_dir(dir)
    json_filename = "{}/{}.json".format(dir, asset_id)
    try:
        with open(json_filename) as json_file:
            # raw = json.load(json_file)
            # raw = json_file.read()

            # clearout the raw data
            raw = json.dumps(json.load(json_file))
    except FileNotFoundError:
        return json.dumps({'status': 'error', 'message': 'not found'})
    return raw


def load_file(json_filename, dir):
    """ open json file and add extra attributes """
    check_dir(dir)
    try:
        with open(json_filename) as json_file:
            raw = json.load(json_file)
    except FileNotFoundError:
        return "not found"

    if 'status' not in raw.keys():
        return "failed"
    try:
        if raw['status'] == 'success':
            raw['item']['file_date'] = time.strftime('%Y-%m-%d %H:%M:%S',
                                                     time.localtime(getmtime(
                                                         json_filename)))
            raw['item']['latest'] = find_latest(dir)
            return raw['item']
    except KeyError:
        return "failed"
    return raw['status']


def get_data(filename, dir):
    """ get keys from dict """
    data = load_file(filename, dir)

    #  not valid - return status
    if type(data) == 'string':
        return data

    output = {}
    for jkey in config.JSON_KEYS:
        if jkey in data:
            output[jkey] = data[jkey]
        else:
            output[jkey] = ''
    return (create_row(output), )


def resize_thumbnail(thumbnail):
    """ calculate thumbnail dimensions """
    # image and description
    thumb = thumbnail["url"]
    prop_w = eval(thumbnail["srcw"])
    prop_h = eval(thumbnail["srch"])
    # thumbnail height
    dsth = 100
    if prop_w > prop_h:
        dstw = round(dsth * (prop_h/prop_w))
    else:
        dstw = round(dsth * (prop_h/prop_w))
    img = """https://r-scale-b6.dcs.redcdn.pl/scale/o2/tvn/\
web-content/m/{}?srcx=0&type=1&srcmode=1&quality=95&\
dstw={}&dsth={}""".format(thumb, dstw, dsth)
    return img


def check_cache(asset_id, img_link):
    """ check if file is already downloaded """
    # TODO: test json files

    result = False
    local_img = '{}/{}.jpg'.format(config.CACHE_DIR, asset_id)
    if not isfile(local_img):
        result = get_image(img_link, local_img)
    else:
        result = True
    if result:
        return local_img
    return ''


def load_image(asset_id, thumbnail):
    """ get image for episode """
    img_link = resize_thumbnail(thumbnail)
    if img_link is None or len(img_link) == 0:
        return ''
    return check_cache(asset_id, img_link)


def get_link(data, quality='HD'):
    """ parse video url for quality """
    try:
        content = data['videos']['main']['video_content']
        if len(content) == 0:
            return None
        for profile in content:
            if profile['profile_name'] == quality:
                return profile['url']
    except KeyError:
        return None
    return None
    # hd = '<span class="hd">(<a href="' + v["url"] + '">LQ</a>)</span>';


def get_desc(data):
    """ truncate description """
    limit = 270

    if len(data) > limit:
        suff = '...'
    else:
        suff = ''
    return '{}{}'.format(data[:limit], suff)


def create_row(data):
    """ format table row output """
    # asset, title, episode, date, thumb, desc, links
    output = {}
    try:
        output[0] = (data['asset_id'], data['id'])
        output[1] = data['serie_title']
        output[2] = "{:02d}".format(data['episode'])
        output[3] = "{:02d}".format(data['season'])
        output[4] = (data['start_date'], data['file_date'])
        output[5] = load_image(data['id'], data['thumbnail'][0])
        # output[5] = resize_thumbnail(data['thumbnail'][0])
        output[6] = get_desc(data['lead'])
        output[7] = (None, 'N/A')
        output[8] = (None, 'N/A')
        output[9] = data['run_time']
        output[10] = str(data['id']) in str(data['latest'])
    except ValueError:
        return None
    # TODO: links
    quality = 'HD'
    remote_link = get_link(data, quality)
    if remote_link is not None:
        output[7] = (remote_link, quality)
        # local link is only available when remote is
        output[8] = ('#', 'LaEp.mp4')
    return output


def find_latest(dir):
    """  return latest file name """
    list_of_files = glob.glob('{}/*.json'.format(dir))
    latest_file = max(list_of_files, key=getmtime)
    return latest_file
