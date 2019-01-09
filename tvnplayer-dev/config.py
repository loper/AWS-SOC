""" settings for player """

PLAYER_URL = 'http://tvnplayer.pl/api/?platform=ConnectedTV&terminal=Panasonic&format=json&\
authKey=064fda5ab26dc1dd936f5c6e84b7d3c2&v=3.1&m=getItem&id='

STATIC_DIR = "static"
DATA_DIR = "data"

CACHE_DIR = "{}/cache".format(STATIC_DIR)
JSON_DIR = "{}/json".format(DATA_DIR)

JSON_KEYS = ('asset_id', 'id', 'start_date', 'serie_title', 'season',
             'episode', 'thumbnail', 'lead', 'videos', 'file_date',
             'run_time', 'latest')
