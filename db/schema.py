import psycopg2 #type: ignore

def create_tables(cursor):
    cursor.execute('DROP TABLE IF EXISTS audio_features;')
    cursor.execute('DROP TABLE IF EXISTS tracks;')
    cursor.execute('DROP TABLE IF EXISTS artists;')
    cursor.execute('DROP TABLE IF EXISTS playlists;')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            artist_id TEXT PRIMARY KEY,
            name TEXT
        ); ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS playlists (
            playlist_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            total_tracks INTEGER,
            source_tag varchar(20),
            description TEXT
        );  ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY,
            track_name TEXT NOT NULL,
            artist_id TEXT,
            playlist_id TEXT,
            FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
            FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id)
        ); ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audio_features (
            track_id TEXT PRIMARY KEY,
            acousticness FLOAT,
            danceability FLOAT,
            energy FLOAT,
            instrumentalness FLOAT,
            liveness FLOAT,
            loudness FLOAT,
            speechiness FLOAT,
            tempo FLOAT,
            valence FLOAT,
            FOREIGN KEY (track_id) references tracks(track_id)
        ); ''')
    
