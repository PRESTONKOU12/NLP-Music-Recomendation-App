def insert_artist(cursor, artist):
    cursor.execute('''
        INSERT INTO artists (artist_id, name) 
            VALUES (%s, %s) 
            ON CONFLICT (artist_id) DO NOTHING;''', 
    (artist['id'], artist['name']))

def insert_track(cursor, track, playlist_id):
    cursor.execute('''
        INSERT INTO tracks (track_id, track_name, artist_id, playlist_id)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (track_id) DO NOTHING;''',
    (track['id'], track['name'], track['artists'][0]['id'], playlist_id))

def insert_playlist(cursor, playlist):
    cursor.execute('''
        INSERT INTO playlists (playlist_id, name, total_tracks, source_tag, description)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (playlist_id) DO NOTHING''',
    (playlist['id'], playlist['name'], playlist['total_tracks'], playlist['source_tag'], playlist['description']))

def insert_audio_features(cursor, af):
    cursor.execute("""
        INSERT INTO audio_features (
            track_id, acousticness, danceability, energy, instrumentalness, liveness, loudness, 
            speechiness, tempo, valence
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (track_id) DO NOTHING;
    """, (
        af['id'], af['acousticness'], af['danceability'], af['energy'], af['instrumentalness'], af['liveness'], af['loudness'],
        af['speechiness'], af['tempo'], af['valence']
    ))