import os
import sys
import json
import shutil
import asyncio
import requests

import platform

__version__ = "v0.2.0"


HELP_TEXT = ("\
usage: vidsrc-search <command> [option] [flags]     \n\
                                                    \n\
available commands:                                 \n\
    help        shows this menu                     \n\
    search      search a movie by name              \n\
    library     actions regarding the movie lib     \n\
                                                    \n\
use 'vidsrc-search help <command>' for info on a    \n\
specific command. arguments are strictly parsed in  \n\
the order specified above                           \
")


HELP_HELP = ("\
usage: vidsrc-search help [option]                  \n\
                                                    \n\
available options:                                  \n\
    help        shows detailed help for 'help'      \n\
    search      shows detailed help for 'search'    \n\
    library     shows detailed help for 'library'   \n\
                                                    \n\
example:                                            \n\
     vidsrc-search help library                     \n\
     vidsrc-search help help                        \
")


HELP_SEARCH = ("\
usage: vidsrc-search search <option> [flags]        \n\
                                                    \n\
required option:                                    \n\
    <str>       a movie title that you would like   \n\
                vidsrc-search to search for         \n\
                                                    \n\
optional flags:                                     \n\
    --raw       when this flag is specified, the    \n\
                program won't do any preprocessing  \n\
                to the html                         \n\
    --new       when this flag is specified, the    \n\
                program will re-cache the html to   \n\
                your computer from vidsrc.to        \n\
                                                    \n\
example:                                            \n\
    vidsrc-search search 'oppenheimer'              \n\
    vidsrc-search search 'avatar'                   \n\
                                                    \n\
the optional flags will have no effect with         \n\
commands other than 'search'                        \
")


HELP_LIB = ("\
usage: vidsrc-search library <option>               \n\
                                                    \n\
required options:                                   \n\
    size        prints the program's disk usage     \n\
    remove      removes the movies library          \n\
    download    downloads the latest movies library \n\
                from https://vidsrc.to              \n\
                                                    \n\
example:                                            \n\
    vidsrc-search library download                  \
")


def show_help():
    print(HELP_TEXT)
    return


def show_help_help():
    print(HELP_HELP)
    return
    
    
def show_help_search():
    print(HELP_SEARCH)
    return
    
    
def show_help_lib():
    print(HELP_LIB)
    return


def show_version():
    print(f"vidsrc-search {__version__}")
    print(f"{platform.python_implementation().lower()} {platform.python_version().lower()}")
    print(f"{platform.platform(True, True).lower()} {platform.machine().lower()}")
    return


def make_directory(path: str) -> None:
    os.makedirs(path, exist_ok=True)
    

def delete_directory_recursive(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
        
        
def asyncio_patch() -> None:
    if sys.platform in ["win32", "cygwin", "msys"]:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        

def check_internet() -> None:
    print("info: verifying internet connection")
    
    try: 
        print("info: testing connection by pinging google.com")
        r = requests.get("https://google.com", allow_redirects = False)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print() 
        print(f"fatal: an http error was encountered")
        print(f"fatal: this might be due to an issue with the external server")
        print(f"fatal: vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.SSLError:
        print() 
        print(f"fatal: could not establish secure connection")
        print(f"fatal: you might be on a monitored network or using a VPN/Proxy")
        print(f"fatal: vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.ConnectionError:
        print()
        print(f"fatal: could not establish internet connection")
        print(f"fatal: make sure you are connected to the internet")
        print(f"fatal: vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.RequestException as e:
        print()
        print(f"fatal: an unknown network error occurred: {e}")
        print(f"fatal: this could be due to an issue with the external server")
        print(f"fatal: vidsrc-search terminating with exit code 255")
        sys.exit(255)

    try:
        print("info: testing connection by pinging vidsrc.to")
        requests.get("https://vidsrc.to", allow_redirects = False)
    except requests.exceptions.HTTPError:
        print() 
        print(f"fatal: an http error was encountered while pinging vidsrc.to")
        print(f"fatal: this might be due to an issue with the external server")
        print(f"fatal: vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.ConnectionError:
        print()
        print(f"fatal: could not reach vidsrc.to")
        print(f"fatal: this might be because of an issue with the")
        print(f"       external server, or it might be due to")
        print(f"       that the server is blocked in your region. ")
        print(f"fatal: vidsrc-search terminating with exit code -1")
        sys.exit(127)
    except requests.exceptions.RequestException as e:
        print()
        print(f"fatal: an unknown network error occurred: {e}")
        print(f"fatal: this could be due to an issue with the server")
        print(f"fatal: vidsrc-search terminating with exit code 255")
        sys.exit(255)
    return


def cleanup() -> None:
    print("info: performing program cleanup process")
    path_one = os.path.expanduser("~/.local/vidsrc-search/movie_buffer")
    path_two = os.path.expanduser("~/.local/vidsrc-search/tv_buffer")
    delete_directory_recursive(path_one)
    delete_directory_recursive(path_two)
    delete_directory_recursive(os.path.expanduser("~/.config/pymovie")) # Pre v0.1.4 folder
    return


def bootstrap() -> None:
    required_path_one = os.path.expanduser("~/.local/vidsrc-search/movie_buffer")
    required_path_two = os.path.expanduser("~/.local/vidsrc-search/tv_buffer")
    required_path_three = os.path.expanduser("~/.local/vidsrc-search/cache")
    make_directory(required_path_one)
    make_directory(required_path_two)
    make_directory(required_path_three)
    return


def load_json(path: str) -> list:
    ret: list = []
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return ret
    with open(path, "r") as f:
        try:
            ret.append(json.load(f))
            return ret
        except json.JSONDecodeError:
            return []


def parse_entry(page: dict) -> list:
    ret: list = []
    for entry in page["result"]["items"]:
        if "embed_url_imdb" in entry:
            ret.append(entry)
    return ret


def unite_jsons(movie_index: int, tv_index: int) -> int:
    print()
    print(f"infno: uniting {movie_index + tv_index} json files")
    unparsed_entries = []
    parsed_entries = []
    for i in range(movie_index):
        unparsed_entries.append(load_json(f"~/.local/vidsrc-search/movie_buffer/{i}.json"))
    for i in range(tv_index):
        unparsed_entries.append(load_json(f"~/.local/vidsrc-search/tv_buffer/{i}.json"))

    print(f"info: parsing {movie_index + tv_index} json files")
    for page in unparsed_entries:
        parsed_entries += parse_entry(page[0])

    print("info: dumping parsed json")
    path = os.path.expanduser("~/.local/vidsrc-search/lib.json")
    with open(path, "w") as f:
        json.dump(parsed_entries, f)
    return len(parsed_entries)
