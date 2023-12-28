import json
import requests
spark_tracks_url = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
base_url = "https://cdn.qstv.on.epicgames.com/"
spark_req = requests.get(spark_tracks_url)
def getSongs():
    songsList = []
    data = spark_req.json()
    for item in data:
        if not item.startswith("_") and item != "lastModified":
            name = data[item]["track"]["tt"]
            artist = data[item]["track"]["an"]
            qi = json.loads(data[item]["track"]["qi"])
            song_id = qi["sid"]
            preview_id = qi["pid"]
            song_url = base_url + song_id
            preview_url = base_url + preview_id
            r = requests.get(song_url)
            song_full_id = r.json()["metadata"]["baseUrls"][0].rsplit("/")[-3]
            r = requests.get(preview_url)
            preview_full_id = r.json()["metadata"]["baseUrls"][0].rsplit("/")[-3]
            print(f'Grabbing link to {artist} - {name}...')
            song = [artist, name, f'Song: https://cdn.fortnite-api.com/streams/{song_full_id}/en.m4a', f"Preview: https://cdn.fortnite-api.com/streams/{preview_full_id}/en.m4a"]
            songsList.append(song)
            #songsList.append(f'{artist} - {name}\nSong: https://cdn.fortnite-api.com/streams/{song_full_id}/en.m4a\nPreview: https://cdn.fortnite-api.com/streams/{preview_full_id}/en.m4a\n\n')
    return songsList