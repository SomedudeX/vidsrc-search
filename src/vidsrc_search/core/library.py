# Using classes for better organization

import os
import sys
import json
import time
import asyncio

import aiohttp
import requests

from .. import utils
from .. import term
from ..term import Logger, ansi_code_patch, supports_unicode
from ..argparsing import ArgumentsError

ansi_code_patch()

# Must import tqdm after ansi code filter has been enabled. This
# prevents tqdm from printing garbage to the console if the console
# does not have support for ansi escape sequences
from tqdm import tqdm
from typing import Any, Dict, List, Union

LogLibrary = Logger()


class BarShell(tqdm):
    """This class is an empty placeholder for when we do not
    want to show the progress bar but still want the rest of the
    program/module to work (e.g. when we are debug logging)
    """
    def __init__(*args, **kwargs) -> None: ...
    def set_description_str(*args, **kwargs) -> None: ...
    def update(*args, **kwargs) -> Union[bool, None]: ...
    def close(*args, **kwargs) -> None: ...


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
            print(" • library does not exist")
            print(" • please download the library first by using 'vidsrc-search library download'")
            print(" • vidsrc-search terminating with exit code 2")
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
        self.progress: Union[BarShell, tqdm] = BarShell()
        if not supports_unicode():
            self.bar_symbol = "·—"
        else:
            self.bar_symbol = "─━"

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
        if LogLibrary.emit == False:
            print(" • initializing library download")
            term.check_tty()
            self.progress = tqdm(
                total=(len(self.types) * 14) + 3,
                desc="initializing",
                leave=False,
                ascii=self.bar_symbol,
                bar_format=" • {desc} {bar} {percentage:.2f}% • {n_fmt}/{total} steps",
                ncols=85
            )
        else:
            term.check_tty()

        start_time = time.time()
        for item in self.types:
            size = self.get_download_size(item)
            asyncio.run(self.download(size, item))

            self.final_size += size * 15
            self.expected_size += utils.unite_jsons(f"~/.local/vidsrc-search/{item}_buffer/", f"~/.local/vidsrc-search/{item}.json")
        end_time = time.time()

        self.progress.set_description_str("cleaning files")
        RemovalManager.remove_library()   # Removing previously downloaded library
        LogLibrary.log("moving new library in place")
        utils.unite_jsons(f"~/.local/vidsrc-search/", f"~/.local/vidsrc-search/lib.json", raw=False)

        self.progress.update(1)
        self.time = end_time - start_time
        self.progress.set_description_str("library download complete")
        self.progress.close()
        return

    def print_summary(self) -> None:
        """Prints the summary of download"""
        loss = 100 * ((self.expected_size - self.final_size) / self.expected_size)
        if loss < 1:
            loss = 0
        print(f" • total number of links to movies downloaded: {self.expected_size}")
        print(f" • estimated link loss from connection issues: ~{loss:.2f}%")
        print(f" • operation took {self.time:.2f} seconds to complete")
        print(f" • vidsrc library has been downloaded")
        return

    def get_download_size(self, kind: str) -> int:
        """Estimates the number of pages (links) of a download using binary
        search.
        """
        self.progress.set_description_str(f"calculating {kind} items")
        LogLibrary.log(f"starting download size estimation for {kind}")

        requests_errors = 0

        index = 0
        width = 2048
        this_direction = 1
        last_direction = 1
        while width > 1:
            url = f"https://vidsrc.to/vapi/{kind}/new/{index}"
            try:
                file = requests.get(url)
            except requests.RequestException as e:
                LogLibrary.log(f"{type(e).__name__.lower()}: {str(e).lower()}")
                LogLibrary.log(f"the above error occured during size estimation of {kind}")
                requests_errors += 1
                if requests_errors >= 10:
                    print(f" • too many errors during size estimation of {kind}")
                    print(f" • vidsrc-search terminating with error code 16")
                    sys.exit(16)
                continue
            if last_direction != this_direction:
                self.progress.update(1)
                width = width // 2
                LogLibrary.log(f"link estimation improved: now at ±{width}")
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
                    LogLibrary.log(f"retry succesful")
                return await response.json()
            LogLibrary.log(f"bad connection detected: retrying ({_tries})")
            if _tries != 0:
                return await DownloadManager.fetch_downloads(session, url, _tries - 1)
            LogLibrary.log(f"too many retries: omitting current link")
            return

    async def download(self, total: int, type: str):
        """Downloads the movie library into a buffer folder on disk"""
        domain = f"https://vidsrc.to/vapi/{type}/new/"
        folder = f"~/.local/vidsrc-search/{type}_buffer/"
        urls = [f"{domain}{i}" for i in range(total)]
        LogLibrary.log(f"initiating downloads with {total} links to {type}s")

        self.progress.update(1)
        async with aiohttp.ClientSession() as session:
            self.progress.set_description_str("waiting for server responses")
            LogLibrary.log(f"adding fetch_downloads() tasks to task list")
            tasks = [DownloadManager.fetch_downloads(session, url) for url in urls]
            LogLibrary.log(f"awaiting tasks")
            jsons = await asyncio.gather(*tasks)
            folder = os.path.expanduser(folder)

            self.progress.update(1)
            LogLibrary.log(f"writing downloaded json files")
            for index, file in enumerate(jsons):
                f = open(f"{folder}{index}.json", "w")
                f.write(json.dumps(file))
                f.close()
        return


class RemovalManager:
    """A manager for removing various items on disk"""

    @staticmethod
    def remove_library() -> None:
        """Removes the library downloaded from vidsrc"""
        LogLibrary.log(f"removing downloaded library json file")
        utils.rmfile(Library.lib_path)
        return

    @staticmethod
    def remove_cache() -> None:
        """Removes the cached html storage"""
        LogLibrary.log(f"removing html cache folder")
        utils.rmdir_recurse(Library.cache_path)
        return

    @staticmethod
    def remove_buffer() -> None:
        """Removes the buffer storage"""
        LogLibrary.log(f"removing download buffering folders")
        folders = utils.get_file(f"~/.local/vidsrc-search", "_buffer")
        for folder in folders:
            utils.rmdir_recurse(f"~/.local/vidsrc-search/" + folder)
        return

    def handle_remove_library(self) -> None:
        """Handles the removal of library"""
        LogLibrary.log(f"initiating handle_remove_libary()")
        if not os.path.exists(Library.lib_path):
            print(" • library does not exist")
            print(" • please download the library first by using 'vidsrc-search library download'")
            print(" • vidsrc-search terminating with exit code 2")
            sys.exit(2)
        with open(Library.lib_path, "r") as f:
            LogLibrary.log(f"loading library json for movie link estimation")
            jsons = json.load(f)

        term.check_tty()

        confirm = input(f" > are you sure you want to remove ~{len(jsons) * 15} links to movies? (Y/n) ")
        if not confirm == "Y":
            print(" • user declined operation")
            print(" • vidsrc-search terminating per user request")
            sys.exit(0)
        print(f" • removing library and cache files")
        RemovalManager.remove_library()
        RemovalManager.remove_cache()
        return


class SizeManager:
    """A manager for printing the size occupied by the program"""

    def __init__(self) -> None:
        """Initializes a SizeManager by calculating the library size"""
        LogLibrary.log(f"getting library folder size recursively")
        self.size = utils.get_folder_size_recursive(Library.root_path)
        return

    def print_size(self) -> None:
        print(f" • total disk usage by vidsrc-search: {self.size}")
        return


def run_module(modules: List[str], args: Dict[str, Any]) -> None:
    """Runs the library module"""
    if modules == ["library", "download"]:
        downloader = DownloadManager(["movie", "tv"])
        downloader.handle_download_library()
        return
    if modules == ["library", "remove"]:
        remover = RemovalManager()
        remover.handle_remove_library()
        return
    if modules == ["library", "size"]:
        sizer = SizeManager()
        sizer.print_size()
        return
    raise ArgumentsError(f"invalid arguments for command 'library' received: {' '.join(modules)}")
