# db/__init__.py

from .schema import create_tables
from .insert import insert_artist, insert_playlist, insert_track, insert_audio_features

__all__ = ['create_tables', 'insert_artist', 'insert_track', 'insert_playlist', 'insert_audio_features']