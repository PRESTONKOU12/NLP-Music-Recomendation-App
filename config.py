import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Spotify
SPOTIFY_CLIENT_ID = config['SpotipyAPI']['client_id']
SPOTIFY_CLIENT_SECRET = config['SpotipyAPI']['client_secret']


# PostgreSQL
DB_PARAMS = {
    'host': config['postgres']['hostname'],
    'port': config['postgres']['portID'],
    'dbname': config['postgres']['dbName'],
    'user': config['postgres']['user'],
    'password': config['postgres']['password']
}