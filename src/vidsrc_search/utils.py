# Any function that does not belong in a specific file goes here. This file is
# not grouped in any particular order.

import os
import re
import sys
import json
import shutil
import asyncio
import requests

from typing import Any, Dict, List
from .term import Logger
from .core.library import RemovalManager

LogUtils = Logger()


def rmdir_recurse(path: str) -> None:
    """Uses shutil to delete directories recursively"""
    path = os.path.expanduser(path)
    if os.path.exists(path):
        shutil.rmtree(path)
    return


def rmfile(path: str) -> None:
    """Uses os.remove to delete a file"""
    path = os.path.expanduser(path)
    if os.path.exists(path):
        os.remove(path)
    return


def get_file(path: str, extension: str) -> List[str]:
    """Gets all files in the path that has the specified extension"""
    files = []
    for (_, dirnames, filenames) in os.walk(os.path.expanduser(path)):
        files.extend(filenames)
        files.extend(dirnames)
        files = [file for file in files if file.endswith(extension)]
        break
    for file in files:  # Function does not add a '/'. Bug-prone point
        file = path + file
    return files


def get_folder_size_recursive(folder_path: str) -> str:
    """Recursively explore a folder to return the size of it"""
    total_size = 0
    folder_path = os.path.expanduser(folder_path)
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)

    units = ["bytes", "kb", "mb", "gb", "tb"]
    for unit in units:
        if total_size < 1024:
            return f"{total_size:.2f} {unit}"
        total_size /= 1024
    return f"{total_size:.2f} {units[len(units) - 1]}"


def cleanup() -> None:
    """Removes buffer directories created during the execution of the program"""
    LogUtils.log(f"performing program cleanup sequence")
    rmdir_recurse(os.path.expanduser("~/.config/pymovie")) # Pre v0.1.4 folder
    rmfile("~/.local/vidsrc-search/movie.json")
    rmfile("~/.local/vidsrc-search/tv.json")
    RemovalManager.remove_buffer()
    return


def initialize(args: Dict[str, Any]) -> None:
    """Called when the program first starts. Prepares program for execution"""
    if args["dbg"]:
        import platform
        global LogUtils
        from .core.version import __version__
        from .term import enable_debug

        enable_debug()
        LogUtils.log(f"vidsrc-search {__version__}")
        LogUtils.log(f"{platform.python_implementation().lower()} {platform.python_version().lower()}")
        LogUtils.log(f"{platform.platform(True, True).lower()} {platform.machine().lower()}")
    LogUtils.log("initializing directories")
    required_path_one = os.path.expanduser("~/.local/vidsrc-search/movie_buffer")
    required_path_two = os.path.expanduser("~/.local/vidsrc-search/tv_buffer")
    required_path_three = os.path.expanduser("~/.local/vidsrc-search/cache")
    os.makedirs(required_path_one, exist_ok=True)
    os.makedirs(required_path_two, exist_ok=True)
    os.makedirs(required_path_three, exist_ok=True)

    if sys.platform in ["win32", "cygwin", "msys"]:  # Windows has some issues with asyncio
        LogUtils.log("patching windows asyncio")
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return


def check_internet() -> None:
    """Verify computer internet connection"""
    try:
        ping_url_one = "https://google.com"
        ping_url_two = "https://vidsrc.to"
        LogUtils.log(f"checking internet connection by pinging {ping_url_one}")
        p1 = requests.get(ping_url_one, allow_redirects=False)
        p1.raise_for_status()
        LogUtils.log(f"checking internet connection by pinging {ping_url_two}")
        p2 = requests.get(ping_url_two, allow_redirects=False)
        p2.raise_for_status()
    except requests.exceptions.RequestException as e:
        name = re.sub(r"(?<!^)(?=[A-Z])", " ", type(e).__name__).lower()
        print(f"• an unknown network error occurred: {name}")
        print(f"• vidsrc-search terminating with exit code 255")
        sys.exit(255)
    return


def unite_jsons(folder_path: str, dest_path: str, raw: bool = True) -> int:
    """Unites all movie/tv show json files from a folder and dumps them to
    another folder. Returns the number of entries parsed.
    """
    folder_path = os.path.expanduser(folder_path)
    dest_path = os.path.expanduser(dest_path)
    LogUtils.log(f"uniting jsons from {folder_path} (raw={raw})")

    files = get_file(folder_path, ".json")
    for index, value in enumerate(files):
        files[index] = folder_path + value

    if raw:
        parsed_entries = []
        unparsed_entries = []
        for file in files:
            unparsed_entries.append(load_json(file))
        for entry in unparsed_entries:
            parsed_entries += parse_entry(entry)
    else:
        parsed_entries = []
        unparsed_entries = []
        for file in files:
            unparsed_entries.append(load_json(file))
        for item in unparsed_entries:
            parsed_entries += item

    LogUtils.log(f"dumping united jsons to {dest_path}")
    with open(dest_path, "w") as file:
        json.dump(parsed_entries, file)
    return len(parsed_entries)


def load_json(path: str) -> List[Any]:
    """Loads a json file into a list and returns it. Returns an empty json file
    if the file does not exist or is invalid.
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return []


def parse_entry(page: Dict) -> List:
    """Parses an entry from a page downloaded from vidsrc"""
    ret: List = []
    for entry in page["result"]["items"]:
        if "embed_url_imdb" in entry:
            ret.append(entry)
    return ret
