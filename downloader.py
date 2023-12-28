import sys
import requests
import os
from pathlib import Path
import json
import song_grabber

songs = song_grabber.getSongs()
songsPath = "Songs"
previewPaths = "Previews"

# i = 0
# while i < len(songs):
#     newlist = [songs[i].strip().split(" - ")[1],songs[i].strip().split(" - ")[0],songs[i+1].strip(),songs[i+2].strip()]
#     songs.append(newlist)
#     i += 4


for song in songs:
    songFolder = Path(f"{songsPath}/{song[0]}")
    songFolder.mkdir(exist_ok=True,parents=True)
    if os.path.exists(songFolder / Path(song[0]+".m4a")):
        print(f"File {song[1]} exists. Skipping...")
        continue
    songPath = songFolder / Path(song[1]+".m4a")
    f = songPath.open("wb")
    print(f"Downloading {song[1]}...")
    request = requests.get(song[2].replace("Song: ",""))
    f.write(request.content)
    f.close()
