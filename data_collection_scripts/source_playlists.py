import spotipy #type: ignore
import json
from config.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import requests #type: ignore
from bs4 import BeautifulSoup #type: ignore

sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

url = "https://blacksunshinemedia.com/featured-articles/list-of-rock-genres/"

def get_genres():
    response = requests.get(url)
    response.raise_for_status()  # Raise error if request failed

    soup = BeautifulSoup(response.text, "html.parser")

    # Inspecting the page, bullet points are inside <ul> and <li> tags.
    # Let's find all <ul> elements and extract text from <li>
    all_bullets = []

    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            text = li.get_text(strip=True)
            if text and len(text) < 20:  # skip empty
                all_bullets.append(text)

    # Optionally, print or save unique genres
    return list(set(all_bullets))



def search_playlists_by_keyword(keyword):
    # Use Spotify API to search for playlists by keyword
    results = sp.search(q=keyword, type='playlist', limit=5)
    playlists = []
    for item in results['playlists']['items']:
        if item is not None:
            playlists.append({
                'name': item['name'],
                'id': item['id'],
                'url': item['external_urls']['spotify'],
                'source_tag': keyword,
                'description': item['description'],
                'total_tracks': item['tracks']['total']  # individual playlist track count
            })
    return playlists

if __name__ == "__main__":
    keywords = get_genres()
    all_playlists = []

    for kw in keywords:
        print(f'Searching Keyword: {kw}')
        playlists = search_playlists_by_keyword(kw)
        all_playlists.extend(playlists)
    
    unique_playlists = {p['url']: p for p in all_playlists}.values()
    with open('playlists.json', 'w') as f:
        json.dump(list(unique_playlists), f, indent=2)
    print(f"Saved {len(unique_playlists)} playlists to data/playlists.json")

