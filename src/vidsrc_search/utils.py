# Any function that does not belong in a specific file goes here. This file is
# not grouped in any particular order.

import os
import re
import sys
import json
import shutil
import asyncio
import requests

from typing import Any, Dict, List, Tuple

from .core.library import RemovalManager

if sys.platform == "win32":
    import ctypes
    import ctypes.wintypes
else:
    import termios


def newline_cursor() -> None:
    """Prints a newline character if the cursor is not at the leftmost column"""
    if cursor_pos()[0] not in ["1", 1]:
        print()
    return


def rmdir_recurse(path: str) -> None:
    """Uses shutil to delete directories recursively"""
    path = os.path.expanduser(path)
    if os.path.exists(path):
        shutil.rmtree(path)
    return

def rmfile(path: str) -> None:
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
    rmdir_recurse(os.path.expanduser("~/.config/pymovie")) # Pre v0.1.4 folder
    rmfile("~/.local/vidsrc-search/movie.json")
    rmfile("~/.local/vidsrc-search/tv.json")
    RemovalManager.remove_buffer()
    return


def initialize() -> None:
    """Called when the program first starts. Prepares program for execution"""
    first_boot_check()
    required_path_one = os.path.expanduser("~/.local/vidsrc-search/movie_buffer")
    required_path_two = os.path.expanduser("~/.local/vidsrc-search/tv_buffer")
    required_path_three = os.path.expanduser("~/.local/vidsrc-search/cache")
    os.makedirs(required_path_one, exist_ok=True)
    os.makedirs(required_path_two, exist_ok=True)
    os.makedirs(required_path_three, exist_ok=True)

    if sys.platform in ["win32", "cygwin", "msys"]:  # Windows has some issues with asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return

def cursor_pos() -> Tuple[Any, Any]:
    """Gets the cursor position from the terminal. Code from stackoverflow (see
    https://stackoverflow.com/a/69582478/23241571) for more info
    """
    if sys.platform == "win32":
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            pass
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        if sys.platform == "win32":
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
    if res:
        return (res.group("x"), res.group("y"))
    return (-1, -1)


def check_internet() -> None:
    """Verify computer internet connection"""
    try:
        print("info: verifying internet connection")
        ping_url_one = "https://google.com"
        ping_url_two = "https://vidsrc.to"
        p1 = requests.get(ping_url_one, allow_redirects=False)
        p2 = requests.get(ping_url_two, allow_redirects=False)
        p1.raise_for_status()
        p2.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"fatal: a network error occured: {type(e).__name__.lower()} {str(e).lower()}")
        print(f"fatal: vidsrc-search terminating with exit code 255")
        sys.exit(255)
    return


def unite_jsons(folder_path: str, dest_path: str, raw: bool = True) -> int:
    """Unites all movie/tv show json files from a folder and dumps them to
    another folder. Returns the number of entries parsed.
    """
    print(f"info: uniting all jsons from '{folder_path}'")

    folder_path = os.path.expanduser(folder_path)
    dest_path = os.path.expanduser(dest_path)
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

    print(f"info: dumping united jsons to '{dest_path}'\n")

    with open(dest_path, "w") as file:
        json.dump(parsed_entries, file, indent=4)
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


def first_boot_check() -> None:
    """Checks whether vidsrc-search is being booted up the first time"""
    if not os.path.exists(os.path.expanduser("~/.local/vidsrc-search")):
        print(
            "\nit seems as though you are opening vidsrc-search for the first time.\n"
            "because of this, you need to complete a ritual before proceeding. \n"
            "please take your right hand and place it on your heart, and type the\n"
            "following and press enter: "
            "\n\n    'i solemnly swear that i am up to no good'"
            "\n"
        )

        message = input(" > ")
        if not message.lower() == "i solemnly swear that i am up to no good":
            print("\nfatal: user failed to complete ritual")
            print("fatal: vidsrc-search terminating with exit code 255")
            sys.exit(255)
        print("\ninfo: ritual succesfully completed by user")
        print("info: rerun vidsrc-search to gain access to the rest of the program")
        print("info: vidsrc-search terminating with exit code 0")
        required_path_one = os.path.expanduser("~/.local/vidsrc-search/movie_buffer")
        required_path_two = os.path.expanduser("~/.local/vidsrc-search/tv_buffer")
        required_path_three = os.path.expanduser("~/.local/vidsrc-search/cache")
        os.makedirs(required_path_one, exist_ok=True)
        os.makedirs(required_path_two, exist_ok=True)
        os.makedirs(required_path_three, exist_ok=True)
        sys.exit(0)
    return
