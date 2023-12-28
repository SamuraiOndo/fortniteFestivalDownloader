import aiohttp
import aiofiles
import asyncio
import time
from pathlib import Path
from song_grabber import get_songs

CHUNK_SIZE = 1024 * 1024 # 1 MB

async def get_file(session, url, directory, name, sem):
    async with sem:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    Path(directory).parents[0].mkdir(
                        parents=True, exist_ok=True)
                    async with aiofiles.open(directory, "wb") as f:
                        async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                            await f.write(chunk)
                    print(f'Downloaded {directory}.')
                else:
                    print(f"not success, code is {resp.status}")
        except asyncio.exceptions.TimeoutError as e:
            print(f"Timed out while getting file {name}.")
        except Exception as e:
            print(f"An error occurred while getting {name}: {e}")

async def verify_file(directory):
    if Path(directory).exists():
        return True
    return False


async def get_files_to_dl(session, items, out_dir):
    sem = asyncio.Semaphore(15) # downloads 15 files at once
    tasks = [asyncio.ensure_future(get_file(session, item[2], f"{out_dir}/{item[0]} - {item[1]}.m4a", f'{item[0]} - {item[1]}.m4a', sem))
             for item in items
             if not await verify_file(f"{out_dir}/{item[0]} - {item[1]}.m4a")]
    return tasks


async def download_files(items, out_dir):
    timeout = aiohttp.ClientTimeout(total=None)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        for _ in range(10):  # verify up to 10 times that the files are valid
            tasks = await get_files_to_dl(session, items, out_dir)
            if len(tasks) == 0:
                print("All files valid!")
                break
            await asyncio.gather(*tasks)
    

async def main():
    start_time = time.time()
    song_list = await get_songs()
    await download_files(song_list, "download")
    print(f"--- {(time.time() - start_time)} seconds to download ---")

if __name__ == "__main__":
    asyncio.run(main())
