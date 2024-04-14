# Using classes for better organization

import os
import sys
import json
import time
import asyncio

import aiohttp
import requests

from typing import Any, List, Union

from .. import utils
from ..argparsing import ArgumentsError


class Library:
    """Properties of the library"""
    root_path = os.path.expanduser("~/.local/vidsrc-search")
    lib_path = os.path.expanduser("~/.local/vidsrc-search/lib.json")
    cache_path = os.path.expanduser("~/.local/vidsrc-search/cache")

    def check_library(
        self,
        exit_on_false: bool = True
    ) -> bool:
        """Checks whether the library exist or not"""
        if os.path.exists(self.lib_path):
            return True
        if exit_on_false:
            print("fatal: library does not exist")
            print("fatal: please download the library first by using 'vidsrc-search library download'")
            print("fatal: vidsrc-search terminating with exit code 2")
            sys.exit(2)
        return False

class DownloadManager:
    """A manager for library downloads"""

    def __init__(
        self,
        types: List[str]
    ) -> None:
        """Initializes a download manager instance with the types of media
        to be downloaded from vidsrc
        """
        self.types = types
        self.time: float

        self.final_size: int = 0
        self.expected_size: int = 0
        return

    def handle_download_library(self) -> None:
        """Handles the downloading of the library"""
        self.start_download()
        self.print_summary()
        return

    def start_download(self) -> None:
        """Starts the downloading of types specified in the constructor"""
        utils.check_internet()

        start_time = time.time()
        for item in self.types:
            size = DownloadManager.get_download_size(item)
            asyncio.run(DownloadManager.download(size, item))

            self.final_size += size * 15
            self.expected_size += utils.unite_jsons(f"~/.local/vidsrc-search/{item}_buffer/", f"~/.local/vidsrc-search/{item}.json")
        end_time = time.time()

        RemovalManager.remove_library()   # Removing previously downloaded libary
        utils.unite_jsons(f"~/.local/vidsrc-search/", f"~/.local/vidsrc-search/lib.json", raw=False)
        utils.cleanup()
        self.time = start_time - end_time
        return

    def print_summary(self) -> None:
        """Prints the summary of download"""
        loss = 100 * ((self.expected_size - self.final_size) / self.expected_size)
        if loss < 1:
            loss = 0
        print(f"info: total/estimated number of movies downloaded: {self.expected_size}/{self.final_size}")
        print(f"info: estimated link loss from client/server connection issues: ~{loss:.2f}%")
        print(f"info: operation took {self.time:.2f} seconds to complete")
        print(f"info: library has been downloaded")
        return

    @staticmethod
    def get_download_size(kind: str) -> int:
        """Estimates the number of pages (links) of a download using binary
        search.
        """
        print(f"info: estimating download size for {kind} items (this may take a while)")

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

    @staticmethod
    async def fetch_downloads(session: aiohttp.ClientSession, url: str, _tries: int = 3) -> Union[Any, None]:
        """Asynchronously fetch a json file from a url, retrying if the response is not a json"""
        async with session.get(url) as response:
            if response.content_type == "application/json":
                if _tries != 3:
                    print(f"info: retry successful")
                return await response.json()
            if _tries != 0:
                print(f"error: bad connection encountered, retrying ({_tries})")
                return await DownloadManager.fetch_downloads(session, url, _tries - 1)
            print(f"info: too many retries, omitting current link")
            return

    @staticmethod
    async def download(total: int, type: str):
        """Downloads the movie library into a buffer folder on disk"""
        domain = f"https://vidsrc.to/vapi/{type}/new/"
        folder = f"~/.local/vidsrc-search/{type}_buffer/"
        urls = [f"{domain}{i}" for i in range(total)]
        print(f"info: initialized {type} download with {total} links to jsons")
        print(f"info: waiting response from {total} server requests")

        async with aiohttp.ClientSession() as session:
            tasks = [DownloadManager.fetch_downloads(session, url) for url in urls]
            jsons = await asyncio.gather(*tasks)
            folder = os.path.expanduser(folder)

            print(f"info: writing json files to disk")
            for index, file in enumerate(jsons):
                f = open(f"{folder}{index}.json", "w")
                f.write(json.dumps(file))
                f.close()
        return


class RemovalManager:
    """A manager for removing various items on disk"""

    @staticmethod
    def remove_library() -> None:
        """Removes the libary downloaded from vidsrc"""
        utils.rmfile(Library.lib_path)
        return

    @staticmethod
    def remove_cache() -> None:
        """Removes the cached html storage"""
        utils.rmdir_recurse(Library.cache_path)
        return

    @staticmethod
    def remove_buffer() -> None:
        """Removes the buffer storage"""
        folders = utils.get_file(f"~/.local/vidsrc-search", "_buffer")
        for folder in folders:
            utils.rmdir_recurse(f"~/.local/vidsrc-search/" + folder)
        return

    def handle_remove_library(self) -> None:
        """Handles the removal of library"""
        if not os.path.exists(Library.lib_path):
            print("fatal: library does not exist")
            print("fatal: please download the library first by using 'vidsrc-search library download'")
            print("fatal: vidsrc-search terminating with exit code 2")
            sys.exit(2)
        with open(Library.lib_path, "r") as f:
            jsons = json.load(f)

        confirm = input(f" > are you sure you want to remove ~{len(jsons) * 15} links to movies? (Y/n) ")
        if not confirm == "Y":
            print("info: user declined operation")
            print("info: vidsrc-search terminating per user request")
            sys.exit(0)
        print(f"info: removing downloaded library")
        print(f"info: removing cached html files")
        RemovalManager.remove_library()
        RemovalManager.remove_cache()
        return


class SizeManager:
    """A manager for printing the size occupied by the program"""

    def __init__(self) -> None:
        """Initializes a SizeManager by calculating the libary size"""
        self.size = utils.get_folder_size_recursive(Library.root_path)
        return

    def print_size(self) -> None:
        print(f"total disk usage by vidsrc-search: {self.size}")
        return


def run_module(arguments: List[str]) -> None:
    """Runs the library module"""
    if arguments == ["library", "download"]:
        downloader = DownloadManager(["movie", "tv"])
        downloader.handle_download_library()
        return
    if arguments == ["library", "remove"]:
        remover = RemovalManager()
        remover.handle_remove_library()
        return
    if arguments == ["library", "size"]:
        sizer = SizeManager()
        sizer.print_size()
        return
    raise ArgumentsError(f"invalid arguments for command 'library' received: {' '.join(arguments)}")
