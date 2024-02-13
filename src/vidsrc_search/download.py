import os
import json
import requests
import asyncio
import aiohttp

from .utils import cleanup

from . import utils
from . import json_utils
    

def get_download_size(kind: str) -> int:
    print(" [Info] Estimating total links (this may take a while)...")
    index = 0
    width = 2048
    this_direction = 1
    last_direction = 1
    while width > 1:
        url = f"https://vidsrc.to/vapi/{kind}/new/{index}"
        file = requests.get(url)
        if last_direction != this_direction:
            width = width // 2
            print(f" [Debug] Estimation got more precise at ±{width}")
        if len(file.content) > 50:
            last_direction = this_direction
            this_direction = 1
            index += width * 1
        if len(file.content) < 50:
            last_direction = this_direction
            this_direction = -1
            index += width * -1
    return index


async def fetch_downloads(session, url):
    async with session.get(url) as response:
        return await response.json()
        

async def download_movies(total: int):
    domain = "https://vidsrc.to/vapi/movie/new/"
    root   = "~/.config/pymovie/movie_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f" [Info] Initiated download_movies with {total} pages")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()
    print(f" [Info] {total} pages/{total * 15} links were succesfully downloaded")


async def download_shows(total: int):
    domain = "https://vidsrc.to/vapi/tv/new/"
    root   = "~/.config/pymovie/tv_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f" [Info] Initiated download_shows with {total} pages")
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()
    print(f" [Info] {total} pages/{total * 15} links were succesfully downloaded")


def handle_download():
    utils.check_internet()
    utils.asyncio_patch()

    movies_size = get_download_size("movie")
    asyncio.run(download_movies(movies_size))
    
    shows_size = get_download_size("tv")
    asyncio.run(download_shows(shows_size))
    
    json_utils.unite_jsons(movies_size, shows_size)
    cleanup()
    return
