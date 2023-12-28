import json
import aiohttp
import asyncio
spark_tracks_url = "https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks"
base_url = "https://cdn.qstv.on.epicgames.com/"

async def get_song_info(item):
    name = item["track"]["tt"]
    artist = item["track"]["an"]
    qi = json.loads(item["track"]["qi"])
    song_id = qi["sid"]
    preview_id = qi["pid"]
    song_url = base_url + song_id
    preview_url = base_url + preview_id
    async with aiohttp.ClientSession() as session:
        r = await session.get(song_url)
        song_full_id = (await r.json())["metadata"]["baseUrls"][0].rsplit("/")[-3]
        r = await session.get(preview_url)
        preview_full_id = (await r.json())["metadata"]["baseUrls"][0].rsplit("/")[-3]
        print(f'Grabbing link to {artist} - {name}...')
        song = [artist, name, f'https://cdn.fortnite-api.com/streams/{song_full_id}/en.m4a', f"https://cdn.fortnite-api.com/streams/{preview_full_id}/en.m4a"]
        return song

async def get_songs():
    async with aiohttp.ClientSession() as session:
        spark_req = await session.get(spark_tracks_url)
        data = await spark_req.json()
        items = [data[item] for item in data if not item.startswith("_") and item != "lastModified"]
        tasks = [asyncio.create_task(get_song_info(item)) for item in items]
        songsList = await asyncio.gather(*tasks)
    return songsList