import os
import sys
import json
import webview
import requests
import webbrowser

from . import utils

from tabulate import tabulate
from thefuzz.fuzz import partial_ratio, ratio


def similarity(str1: str, str2: str) -> float:
    return (5 * partial_ratio(str1, str2) + ratio(str1, str2)) / 6


def relevance_key(entry) -> float:
    return entry["Match"]


def sort_results(result: list) -> list:
    result.sort(key = relevance_key, reverse = True)
    return result


def search_library(search_query: str):
    ret = []
    lib_path = os.path.expanduser("~/.local/vidsrc-search/lib.json")
    if not os.path.exists(lib_path):
        print(" [Fatal] Library does not exist")
        print(" [Fatal] Please download the library first by using 'vidsrc-search library download'")
        print(" [Fatal] Vidsrc-search terminating with exit code 2")
        sys.exit(2)

    with open(lib_path, "r") as f: 
        library = f.read()
    library = json.loads(library) 

    for entry in library: 
        if similarity(entry["title"], search_query) >= 60:
            ret.append({
                "Index": None,
                "Title": entry["title"], 
                "IMDB ID": entry["imdb_id"], 
                "Type": entry["type"], 
                "URL": entry["embed_url_imdb"], 
                "Match": f"{similarity(entry['title'], search_query):.2f}%",
            })

    if len(ret) == 0: 
        return None

    ret = sort_results(ret)
    while len(ret) > 20: 
        del ret[len(ret) - 1]
    index = 1
    for result in ret:
        result["Index"] = f"[{index}]"
        index += 1
    return ret


def on_closing() -> None:
    print(f" [Info] Closing window to vidsrc.to")
    print(f" [Info] Vidsrc-search executed successfully")
    utils.cleanup()
    

def on_loaded() -> None:
    print(" [Info] Opened window to movie")
    webview.windows[0].events.loaded -= on_loaded
    webview.windows[0].on_top = False
    return


def print_warning() -> None:
    print()
    print(" [Warning] The content of the movie is hosted on a third party site. The")
    print("           site is not endorsed by the author or checked for its quality, ")
    print("           content, or authenticity. The author of vidsrc-search disclaims")
    print("           any responsibility, express or implied, of the consequences ")
    print("           as a result your usage or dependence on the website provided ")
    print("           through this tool. ")
    print(" [Warning] The following window shown will be the contents of vidsrc.to\n")
    affirm = input(" > I have read and understood the conditions above (Y/n) ")
    print()
    if not affirm == "Y":
        print()
        print(" [Info] Terminating per user request")
        raise UserWarning
    return


def show_movie(index: int, results: list, fallback: bool = False):
    print_warning()
    utils.check_internet()

    number = index + 1
    title = results[index]["Title"]
    url = results[index]["URL"]
    id = results[index]["IMDB ID"]

    print()
    print(f" [Info] Checking for local cache")

    if not os.path.exists(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html")):
        print(f" [Info] Local cache not found: Getting remote html")
        response = requests.get(url)
        print(f" [Info] Remote html request status code is {response.status_code}")
        with open(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"), "w") as f:
            print(f" [Info] Writing remote html content to local cache")
            f.write(response.content.decode())

    if not fallback:
        print(f" [Info] Opening #{number} '{title}' in new browser window")
        webbrowser.open("file://" + os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"))
        return

    print(f" [Info] Using fallback mode for movie launching")
    print(f" [Info] Opening #{number} '{title}' in new window")
    
    window = webview.create_window(
        f"External - {title}",
        os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"),
        maximized = True,
        on_top = True,
    )

    window.events.closing += on_closing
    window.events.loaded += on_loaded

    webview.start(
        http_server=True,
        storage_path=os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}"),
        private_mode=False
    )
    return
    

def handle_search(query: str, fallback: bool = False) -> None:
    print(f" [Info] Searching json library for '{query}'")
    results = search_library(query)
    if results == None:
        print(f" [Info] '{query}' not found in movies library")
        print(f" [Info] Vidsrc-search terminating due to entry not found")
        return
        
    print()
    print(
        tabulate(
            results,
            headers = "keys",
            tablefmt = "grid",
            maxcolwidths = [4, 36]
        )
    )
    
    print()
    while True:
        try:
            open_index = int(input(" > Choose an index to open in browser: "))
            if open_index <= 0 or open_index > len(results):
                raise ValueError()
            break
        except ValueError:
            print(" [Error] Please enter a valid value")
            continue
    
    open_index -= 1
    show_movie(open_index, results, fallback=fallback)
    return
