import os
import json
import time
import requests
import asyncio
import aiohttp

from .utils import cleanup

from . import utils
from . import json_utils


def get_download_size(kind: str) -> int:
    print()
    print(f" [Info] Estimating total {kind} links (this may take a while)...")
    index = 0
    width = 2048
    this_direction = 1
    last_direction = 1
    while width > 1:
        url = f"https://vidsrc.to/vapi/{kind}/new/{index}"
        file = requests.get(url)
        if last_direction != this_direction:
            width = width // 2
        if len(file.content) > 50:
            last_direction = this_direction
            this_direction = 1
            index += width * 1
        if len(file.content) < 50:
            last_direction = this_direction
            this_direction = -1
            index += width * -1
    return index


async def fetch_downloads(session, url, tries = 3):
    try:
        async with session.get(url) as response:
            if tries != 3:
                print(f" [Info] Retry successful")
            return await response.json()
    except aiohttp.ClientError:
        if tries <= 0:
            print(f" [Error] Exceeded max retries for bad connection: omitting current link")
            return
        print(f" [Error] Bad connection encountered: retrying ({4 - tries})")
        return await fetch_downloads(session, url, tries - 1)

        

async def download_movies(total: int):
    domain = "https://vidsrc.to/vapi/movie/new/"
    root   = "~/.local/vidsrc-search/movie_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f" [Info] Initiated download_movies() with {total} links to jsons")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        print(f" [Info] Waiting response from {total} server requests")
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()

    print(f" [Info] Requests for {total} links to {total * 15} movies were sent and received")
    return


async def download_shows(total: int):
    domain = "https://vidsrc.to/vapi/tv/new/"
    root   = "~/.local/vidsrc-search/tv_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f" [Info] Initiated download_shows() with {total} links to jsons")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        print(f" [Info] Waiting for response from {total} server requests")
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()

    print(f" [Info] Requests for {total} links to {total * 15} movies were sent and received")
    return


def handle_download():
    start = time.time()
    utils.check_internet()
    utils.asyncio_patch()

    movies_size = get_download_size("movie")
    asyncio.run(download_movies(movies_size))
    
    shows_size = get_download_size("tv")
    asyncio.run(download_shows(shows_size))
    
    final_size = json_utils.unite_jsons(movies_size, shows_size)
    expected_size = (movies_size + shows_size) * 15
    cleanup()

    end = time.time()

    print()
    print(f" [Info] Total/expected number of movies downloaded: {expected_size}/{final_size}")
    print(f" [Info] Link loss from client/server connection issues: ~{round((expected_size - final_size)/expected_size, 2)}%")
    print(f" [Info] Operation took {round(start - end, 2)} seconds to complete")
    print(f" [Info] Library has been downloaded")
    return
