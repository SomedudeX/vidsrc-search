import os
import sys
import json
import requests
import webbrowser

from . import utils

from tabulate import tabulate
from thefuzz.fuzz import partial_ratio, ratio
from html.parser import HTMLParser


def similarity(str1: str, str2: str) -> float:
    return (2 * partial_ratio(str1.lower(), str2.lower()) + 8 * ratio(str1.lower(), str2.lower())) / 10


def relevance_key(entry) -> float:
    return float(entry["Match"])


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
        if similarity(entry["title"][:len(entry["title"]) - 7], search_query) >= 60:
            ret.append({
                "Index": None,
                "Title": entry["title"], 
                "IMDB ID": entry["imdb_id"][2:],
                "Type": entry["type"], 
                "URL": entry["embed_url_imdb"],
                "Match": f"{similarity(entry['title'][:len(entry['title']) - 7], search_query):.2f}",
            })

    if len(ret) == 0: 
        return None

    ret = sort_results(ret)
    while len(ret) > 20: 
        del ret[len(ret) - 1]
    index = 1
    for result in ret:
        result["Index"] = f"[{index}]"
        result["Match"] += "%"
        index += 1
    ret.reverse()
    return ret


def ask_open_index(movies: list) -> int:
    while True:
        try:
            open_index = int(input(" > Choose an index to open in browser: "))
            if open_index <= 0 or open_index > len(movies):
                raise ValueError()
            open_index = len(movies) - open_index
            return open_index
        except ValueError:
            print(" [Error] Please enter a valid value")
            continue


def print_movies(movies: list) -> None:
    print()
    print(tabulate(movies, headers = "keys", tablefmt = "grid", maxcolwidths = [4, 36]))
    print()
    return


def print_warning() -> None:
    print()
    print(" [Warning] The content of the movie is hosted on a third party site. The")
    print("           site is not endorsed by the author or checked for its quality, ")
    print("           content, or authenticity. The author of vidsrc-search disclaims")
    print("           any responsibility, express or implied, of the consequences ")
    print("           as a result your usage or dependence on the website provided ")
    print("           through this tool. ")
    print(" [Warning] The following window shown will be the cached contents of vidsrc.to\n")
    affirm = input(" > I have read and understood the conditions above (Y/n) ")
    print()
    if not affirm == "Y":
        print()
        print(" [Info] Terminating per user request")
        raise UserWarning
    return


def delete_substring(text, start_offset, end_offset):
    deleted_text = text[:start_offset - 1] + text[end_offset + 1:]
    return deleted_text


def process_html(path: str) -> None:
    print(f" [Info] Processing html")
    with open(path, "r") as f:
        content = f.readlines()
        content = ''.join(content)
        while True:
            parser = FileProcesser()
            parser.feed(content)
            if len(parser.positions_tag) == 0:
                break
            content = delete_substring(
                content,
                parser.start_positions[0][1] + 1,
                parser.end_positions[0][1] + len(parser.positions_tag[0]) - 1
            )

    print(f" [Info] Writing processed html")
    with open(path, "w") as f:
        f.write(content)


def show_movie(index: int, results: list, raw: bool, recache: bool):
    print_warning()
    utils.check_internet()

    number = index + 1
    title = results[index]["Title"]
    url = results[index]["URL"]
    id = results[index]["IMDB ID"]

    print()
    print(f" [Info] Checking for local cache")
    if os.path.exists(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html")) and recache:
        print(f" [Info] Local cache found: Recaching by requesting remote html per user request")
        response = requests.get(url)
        print(f" [Info] Remote html request status code is {response.status_code}")
        with open(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"), "w") as f:
            print(f" [Info] Writing remote html content to local cache")
            f.write(response.content.decode())
            print(f" [Info] Finished recaching html")
    if not os.path.exists(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html")):
        print(f" [Info] Local cache not found: Caching by requesting remote html")
        response = requests.get(url)
        print(f" [Info] Remote html request status code is {response.status_code}")
        with open(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"), "w") as f:
            print(f" [Info] Writing remote html content to local cache")
            f.write(response.content.decode())
            print(f" [Info] Finished caching html")
    if not raw:
        process_html(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"))
    print(f" [Info] Opening #{number} '{title}' in new browser window")
    webbrowser.open("file://" + os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"))
    return
    

def handle_search(query: str, raw: bool = True, recache: bool = False) -> None:
    print(f" [Info] Searching json library for '{query}'")
    print(f" [Info] Open raw website: {raw}")
    print(f" [Info] Recaching website: {recache}")
    results = search_library(query)
    if results == None:
        print(f" [Info] '{query}' not found in movies library")
        print(f" [Info] Vidsrc-search terminating due to entry not found")
        return
    print_movies(results)
    open_index = ask_open_index(results)
    show_movie(open_index, results, raw, recache)
    return


class FileProcesser(HTMLParser):

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        self.start_positions: list[tuple] = []
        self.end_positions: list[tuple] = []
        self.positions_tag: list[str] = []
        self.current_bad_script = 0
        self.current_bad_element = 0
        super().__init__(convert_charrefs=convert_charrefs)

    def handle_starttag(self, tag, attrs):
        if tag not in ["script", "div"]:
            return
        for attr in attrs:
            if self.bad_script(attr):
                self.current_bad_script += 1
                self.start_positions.append(self.getpos())

    def handle_endtag(self, tag: str) -> None:
        if tag not in ["script", "div"]:
            return
        if self.current_bad_script == 1:
            self.current_bad_script = 0
            self.end_positions.append(self.getpos())
            self.positions_tag.append("</script>")
        if self.current_bad_script != 0:
            self.current_bad_script -= 1

    @staticmethod
    def bad_script(script_attr: tuple):
        if script_attr[0] != "src":
            return False
        if "embed" in script_attr[1]:
            return False
        if "cloudflare" in script_attr[1]:
            return False
        return True
