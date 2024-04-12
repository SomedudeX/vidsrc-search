import os
import sys
import json
import time
import asyncio

import requests
import aiohttp

from . import utils


def get_download_size(kind: str) -> int:
    print()
    print(f"info: estimating total {kind} links (this may take a while)...")
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
                print(f"info: retry successful")
            return await response.json()
    except aiohttp.ClientError:
        if tries <= 0:
            print(f"error: exceeded max retries for bad connection: omitting current link")
            return
        print(f"error: bad connection encountered: retrying ({4 - tries})")
        return await fetch_downloads(session, url, tries - 1)

        

async def download_movies(total: int):
    domain = "https://vidsrc.to/vapi/movie/new/"
    root   = "~/.local/vidsrc-search/movie_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f"info: initiated download_movies() with {total} links to jsons")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        print(f"info: waiting response from {total} server requests")
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()

    print(f"info: requests for {total} links to {total * 15} movies were sent and received")
    return


async def download_shows(total: int):
    domain = "https://vidsrc.to/vapi/tv/new/"
    root   = "~/.local/vidsrc-search/tv_buffer/"
    urls   = [f"{domain}{i}" for i in range(total)]
    print(f"info: initiated download_shows() with {total} links to jsons")

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_downloads(session, url) for url in urls]
        print(f"info: waiting for response from {total} server requests")
        jsons = await asyncio.gather(*tasks)
        root = os.path.expanduser(root)
        for index, file in enumerate(jsons):
            f = open(f"{root}{index}.json", "w")
            f.write(json.dumps(file))
            f.close()

    print(f"info: requests for {total} links to {total * 15} movies were sent and received")
    return


def handle_download():
    start = time.time()
    utils.check_internet()
    utils.asyncio_patch()

    movies_size = get_download_size("movie")
    asyncio.run(download_movies(movies_size))
    
    shows_size = get_download_size("tv")
    asyncio.run(download_shows(shows_size))
    
    final_size = utils.unite_jsons(movies_size, shows_size)
    expected_size = (movies_size + shows_size) * 15
    utils.cleanup()

    end = time.time()

    print()
    print(f"info: total/expected number of movies downloaded: {expected_size}/{final_size}")
    print(f"info: link loss from client/server connection issues: ~{round((expected_size - final_size)/expected_size, 2)}%")
    print(f"info: operation took {round(start - end, 2)} seconds to complete")
    print(f"info: library has been downloaded")
    return


def handle_remove() -> None:
    lib_path = os.path.expanduser("~/.local/vidsrc-search/lib.json")
    cache_path = os.path.expanduser("~/.local/vidsrc-search/cache")
    if not os.path.exists(lib_path):
        print("fatal: library does not exist")
        print("fatal: please download the library first by using 'vidsrc-search library download'")
        print("fatal: vidsrc-search terminating with exit code 2")
        sys.exit(2)
    with open(lib_path, "r") as f:
        jsons = json.load(f)

    confirm = input(f" > are you sure you want to remove ~{len(jsons) * 15} links to movies? (Y/n) ")
    if not confirm == "Y":
        print("info: user declined operation")
        print("info: vidsrc-search terminating per user request")
        sys.exit(0)

    print("info: removing library json file")
    os.remove(lib_path)
    utils.delete_directory_recursive(cache_path)
    print("info: library json file removed")
    return


def get_folder_size_recursive(folder_path):
    total_size = 0
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)
    return total_size


def get_size():
    path = os.path.expanduser("~/.local/vidsrc-search")
    size = get_folder_size_recursive(path)

    units = ["bytes", "kb", "mb", "gb", "tb"]
    index = 0
    while size >= 1024:
        size /= 1024
        index += 1
    print(f"total disk usage by vidsrc-search: {round(size, 2)} {units[index]}")
