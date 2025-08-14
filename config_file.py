import dotenv
import os


dotenv_path = dotenv.find_dotenv() 

dotenv.load_dotenv(dotenv_path)

#SpotifyApi
SPOTIFY_CLIENT_ID = os.getenv("spotify_client_id")
SPOTIFY_CLIENT_SECRET = os.getenv("spotify_client_secret")

# PostgreSQL
DB_PARAMS = {
    'host': os.getenv("hostname"),
    'port': os.getenv("port"),
    'dbname': os.getenv("name"),
    'user': os.getenv("user"),
    'password': os.getenv("password")
}