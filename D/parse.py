import json
import glob
from os.path import getmtime


def run():
    DIR = "data/json"
    result = []

    # find all json files
    for filename in glob.iglob('{}/*.json'.format(DIR),
        recursive=True):
        output = get_data(filename)
        if type(output) == tuple:
            result.append(output[0])
        else:
            print('[error] Getting data from file {}'.format(filename))
            print(output)
    print(result)
    return result


def load_file(json_filename):
    # json_file_name = "{}/{}.json".format(dir, asset_id)

    try:
        with open(json_filename) as json_file:
            raw = json.load(json_file)
    except FileNotFoundError:
        return "not found"

    if 'status' not in raw.keys():
        return "failed"
    if raw['status'] == 'success':
        raw['item']['file_date'] = getmtime(json_filename)
        return raw['item']
    return raw['status']

def get_data(filename):
    KEYS = ('asset_id', 'id', 'start_date', 'serie_title', 'season',
    'episode', 'thumbnail', 'lead', 'videos', 'file_date')

    data = load_file(filename)

    #  not valid - return status
    if type(data) == 'string':
        return data

    output = {}
    for jkey in KEYS:
        if jkey in data:
            output[jkey] = data[jkey]
        else:
            output[jkey] = ''
    return (create_row(output), )

def resize_thumbnail(thumbnail):
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
    img = 'https://r-scale-b6.dcs.redcdn.pl/scale/o2/tvn/web-content/m/{}?srcx=0&type=1&srcmode=1&quality=95&dstw={}&dsth={}'.format(thumb, dstw, dsth)
    return img

def create_row(data):
    # asset, title, episode, date, thumb, desc, links
    output = {}
    output[0] = (data['asset_id'], data['id'])
    output[1] = data['serie_title']
    output[2] = data['episode']
    output[3] = data['season']
    output[4] = (data['start_date'], data['file_date'])
    print(output[3])
    output[5] = resize_thumbnail(data['thumbnail'][0])
    output[6] = data['lead']
    # TODO: links
    output[7] = 'YY'
    return output