import requests  # type: ignore

RECCOBEATS_API_BASE_URL = "https://api.reccobeats.com/v1/audio-features?ids="
payload = {}
headers = {
    'Accept': 'application/json'
}

def get_audio_features_batch(track_ids):
    """
    Fetch audio features for up to 100 Spotify track IDs in one call.
    Returns a dict {track_id: audio_features_dict}
    """
    if not track_ids: #If there are no track Id's passed, return empty json.
        return {}

    ids_str = ",".join(track_ids) #Necesary formating for batched request. 
    request_url = f"{RECCOBEATS_API_BASE_URL}{ids_str}"
    response = requests.get(request_url, headers=headers, data=payload)

    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Unable to process request\nStatus Code {response.status_code}")
        return {}

    # API should return a list of features; index by id for easier lookups
    features_by_id = {}
    if "content" in data and isinstance(data["content"], list):
        for feat, spotify_id in zip(data["content"], track_ids):
            features_by_id[spotify_id] = feat
    return features_by_id

