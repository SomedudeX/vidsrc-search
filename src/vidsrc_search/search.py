import os
import sys
import json
import webbrowser

from tabulate import tabulate
from thefuzz.fuzz import partial_ratio, ratio


def similarity(Str1: str, Str2: str) -> float:
    return (5 * partial_ratio(Str1, Str2) + ratio(Str1, Str2)) / 6


def relevance_key(entry) -> float:
    return entry["Match"]


def sort_results(result: list) -> list:
    result.sort(key = relevance_key, reverse = True)
    return result


def search_library(search_query: str) -> list | None:
    ret = []
    lib_path = os.path.expanduser("~/.config/pymovie/lib.json")
    if not os.path.exists(lib_path):
        print(" [Fatal] Library does not exist")
        print(" [Fatal] Please download the library first by using 'vidsrc-search libary download'")
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
            "Match": f"{round(similarity(entry["title"], search_query), 2)}%",
            })

    if len(ret) == 0: return None
    ret = sort_results(ret)

    while len(ret) > 20: 
        del ret[len(ret) - 1]
        
    index = 1
    for result in ret:
        result["Index"] = f"[{index}]"
        index += 1
    return ret


def handle_search(query: str) -> None:
    print(f" [Info] Searching json libary for '{query}'")
    results = search_library(query)
    if results == None:
        print(f" [Info] '{query}' not found in movies library")
        print(f" [Info] Vidsrc-search terminating due to entry not found")
        return
        
    print()
    print(
        tabulate(
            results,
            headers = "keys"
        )
    )
    
    print()
    while True:
        try:
            open_index = int(input(" > Choose an index to open in browser: "))
            if open_index <= 0 or open_index >= len(results):
                raise ValueError()
            break
        except ValueError:
            print(" [Error] Please enter a valid value")
            continue
    
    open_index -= 1
    
    print()
    print(" [Warning] The content of the movie is hosted on a third party site. The")
    print("           site is not endorsed by the author or checked for its quality, ")
    print("           content, or authenticity. The author of vidsrc-search disclaims")
    print("           all responsibilities, express or implied, of your usage or ")
    print("           dependence on the website provided through this tool")
    print(" [Warning] Ad/privacy and pop-up blockers are highly recommended\n")
    input(" > Press enter to continue ")
    print(f"\n [Info] Opening {open_index} in your default browser")
    
    webbrowser.open(results[open_index]["URL"])
    print(f" [Info] Opened link to movie '{results[open_index]["Title"]}'")
