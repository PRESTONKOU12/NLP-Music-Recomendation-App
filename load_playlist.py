'''
THIS FILE IS USED FOR SCRAPING THROUGH THE SOURCED PLAYLISTS AND ADDING THEM TO A POSTGRES DATABASE. 
TO DO: 
-Extract audio features from tracks and store them. 
'''

#Package imports
import psycopg2 #type: ignore #connect to my postsql database
import spotipy #type: ignore #connect to the spotify api
import json #parce my json playlist file
import time 
import os


#Helper values and functions
from config import DB_PARAMS, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from db import create_tables, insert_artist, insert_track, insert_playlist, insert_audio_features
from audio_features import get_audio_features_batch
from itertools import islice


################# Connect spotify ###########################
def connect_spotify():
    return spotipy.Spotify(
        auth_manager = spotipy.SpotifyClientCredentials(
            client_id = SPOTIFY_CLIENT_ID,
            client_secret = SPOTIFY_CLIENT_SECRET
        )
    )
#############################################################


################# Load Extracted Playlists JSON File ######## 
def load_json(file = 'playlists.json'):
    with open(file, 'r') as data:
        return json.load(data) 
#############################################################


################ CACHE LOAD / WRITING #######################
cache_file = 'cache/loaded_playlists.json'
def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            content = f.read().strip()
            if not content:
                return set()
            # Expecting a list of playlist IDs in the cache file
            return set(json.loads(content))
    return set()

def save_cache(loaded_playlists):
    with open(cache_file, "w") as f:
        json.dump(list(loaded_playlists), f, indent=2)
#############################################################



def chunked_iterable(iterable, size):
    """Yield successive chunks from iterable of given size."""
    it = iter(iterable)
    while True:
        chunk = list(islice(it, size))
        if not chunk:
            break
        yield chunk



def load_playlist_tracks(sp, curr, conn, playlist_id):
    try:
        results = sp.playlist_items(playlist_id, additional_types=['track']) #Gets the results from the spotify api. 
    except spotipy.exceptions.SpotifyException as e:
        print(f"Failed to load playlist {playlist_id}: {e}")
        return
    
    # Extract valid track IDs
    tracks_data = []
    for item in results['items']: #Loops through all of the items in the playlist so we can further batch them.
        track = item['track'] #Gets track information
        if track and track.get('id'):
            tracks_data.append(track)

    # Process in batches of 50–100
    for batch in chunked_iterable(tracks_data, 40): #Chunks the track Id's into groups so we can further process
        track_ids = [t['id'] for t in batch]

        # Insert artists & tracks first
        for track in batch:
            try:
                artist = track['artists'][0]
                if artist and artist.get('id'):
                    insert_artist(curr, artist)
            except Exception as e:
                print(f'Failed to insert artist: {e}')

            try:
                insert_track(curr, track, playlist_id)
            except Exception as e:
                print(f'Failed to insert track: {e}')

        # Fetch all audio features for the batch in one call
        features_map = get_audio_features_batch(track_ids)
        # Insert audio features if found
        for track_id in track_ids:
            if track_id in features_map:
                try:
                    af = features_map[track_id]
                    af["id"] = track_id  # Replace Reccobeats ID with Spotify ID
                    insert_audio_features(cursor=curr, af=af)
                except Exception as e:
                    print(f'Failed to insert audio features for {track_id}: {e}')
            else:
                print(f"No audio features found for track {track_id}")

        conn.commit()  # Commit once per batch
        




############### Main execution flow ###############
if __name__ == "__main__":
    sp = connect_spotify()
    playlists = load_json() #Load my json file into the script for use.
    loaded = load_cache() 

    with psycopg2.connect(**DB_PARAMS) as conn: 
        with conn.cursor() as curr:
            create_tables(curr) # Creates the tables in postgress
            conn.commit() 

            for pl in playlists: #pl = 'playlist' loops through individual playlists in my json file
                playlist_id = pl['id']
                print(f'loading playlist: {pl['name']}')
                
                if playlist_id in loaded: #Check if playlist has already been loaded 
                    print(f'Skipping playlist {playlist_id} (already loaded)\n.')
                    continue
                
                insert_playlist(curr, pl) #Insert playlist into playlist table seperately
                conn.commit()  # Commit after inserting playlist
                load_playlist_tracks(sp, curr, conn, playlist_id)
                
                loaded.add(playlist_id) 
                save_cache(loaded) 
                
                print()
    
