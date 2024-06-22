# Using classes for better organization

import os
import re
import json
import requests
import webbrowser

from .library import Library
from .. import utils
from .. import term
from ..term import Logger
from ..argparsing import ArgumentsError

from typing import Any, Dict, List

from tabulate import tabulate
from thefuzz.fuzz import partial_ratio, ratio

LogSearch = Logger()


class SearchManager:
    """Library search related functions"""

    def __init__(
        self,
        query: str
    ) -> None:
        """Initializes a SearchManager object with a query"""
        self.library = Library()
        self.query: str = query
        self.results: List[Dict] = []
        return

    def search_library(self) -> None:
        """Initiates a library search with the query specified during init"""
        LogSearch.log(f"reading library")
        with open(self.library.lib_path, "r") as f:
            library = f.read()
        library = json.loads(library)

        LogSearch.log(f"checking library entries for potential match")
        for entry in library:
            self.check_entry(entry)
        self.sort_results()

        LogSearch.log(f"processing matched entries")
        while len(self.results) > 20:
            del self.results[len(self.results) - 1]
        for index, result in enumerate(self.results):
            result["Index"] = f"[{index + 1}]"
            result["Match"] += "%"
        self.results.reverse()
        return

    def check_entry(
        self,
        entry: Dict[str, str]
    ) -> None:
        """Checks an entry to see whether the entry has enough similarity with
        specified query to be appended into self.result
        """
        if SearchManager.similarity(entry["title"][:len(entry["title"]) - 7], self.query) >= 60:
            self.results.append({
                "Index": None,
                "Title": entry["title"],
                "IMDB ID": entry["imdb_id"][2:],
                "Type": entry["type"],
                "URL": entry["embed_url_imdb"],
                "Match": f"{SearchManager.similarity(entry['title'][:len(entry['title']) - 7], self.query):.2f}",
            })
        return

    def sort_results(self) -> None:
        """Sorts the result"""
        self.results.sort(key = SearchManager.sort_key, reverse = True)
        return

    @staticmethod
    def similarity(str1: str, str2: str) -> float:
        """Returns the similarity value (0-100%) between two strings"""
        return (2 * partial_ratio(str1.lower(), str2.lower()) + 8 * ratio(str1.lower(), str2.lower())) / 10

    @staticmethod
    def sort_key(entry) -> float:
        """The key to sort with"""
        return float(entry["Match"])


class SearchHandler:
    """Handles the search operation"""

    def __init__(
        self,
        query: str,
        args: Dict[str, Any]
    ) -> None:
        """Initializes a SearchHandler object"""
        self.query = query
        self.results = []

        term.check_tty()

        self.library = Library()
        self.library.check_library()

        self.raw = args["raw"]
        self.new = args["new"]
        self.byid = args["byid"]
        return

    def handle_search(self) -> None:
        """Handles searching the movie library"""
        self.process_query()
        print(f" • searching json library for '{self.query}'")
        print(f" • open raw website: {str(self.raw).lower()}")
        print(f" • recaching website: {str(self.new).lower()}")
        print(f" • search by imdb id: {str(self.byid).lower()}")

        if self.byid:
            self.handle_id()
            return

        self.manager = SearchManager(self.query)
        self.manager.search_library()
        self.results = self.manager.results
        if len(self.results) == 0 :
            print(f" • '{self.query}' not found in movies library")
            print(f" • vidsrc-search terminating due to entry not found")
            return
        self.print_movies()
        open_index = self.ask_open_index()
        self.show_movie(open_index)
        return
    
    def handle_id(self):
        """Handles searching the movie library by imdb id"""
        LogSearch.log(f"reading library")
        with open(self.library.lib_path, "r") as f:
            library = f.read()
        library = json.loads(library)

        LogSearch.log(f"checking library entries for potential match")
        for entry in library:
            if entry["imdb_id"][2:] == self.query:
                print(f" • found a matching entry: {entry["title"]}")
                url = entry["embed_url_imdb"]
                title = entry["title"]
                id = entry["imdb_id"][2:]

        if self.raw:
            LogSearch.log("directly opening vidsrc link in browser")
            print(f" • opening '{title}' in new browser tab")
            webbrowser.open(url)
            return

        if self.new or not os.path.exists(os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html")):
            SearchHandler.cache_movie(url, f"~/.local/share/vidsrc-search/cache/{id}.html")
        SearchHandler.process_html(os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html"))
        print(f" • opening '{title}' in new browser tab")
        webbrowser.open("file://" + os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html"))
        return
        

    def print_movies(self) -> None:
        """Pretty prints the movies in a table"""
        print(
            tabulate(
                self.results,
                headers = "keys",
                tablefmt = "grid",
                maxcolwidths = [4, 36]
            )
        )

    def ask_open_index(self) -> int:
        """Asks the user for the movie to open to"""
        while True:
            try:
                open_index = int(input(" > choose an index to open in browser: "))
                if open_index <= 0 or open_index > len(self.results):
                    raise ValueError()
                open_index = len(self.results) - open_index
                return open_index
            except ValueError:
                print(" • please enter a valid value")
                continue

    def show_movie(self, index: int) -> None:
        """Shows the movie chosen by the user in their browser"""
        SearchHandler.print_warning()
        utils.check_internet()

        LogSearch.log(f"gathering movie information from library")
        title = self.results[index]["Title"]
        url = self.results[index]["URL"]
        id = self.results[index]["IMDB ID"]

        if self.raw:
            LogSearch.log("directly opening vidsrc link in browser")
            print(f" • opening '{title}' in new browser tab")
            webbrowser.open(url)
            return

        if self.new or not os.path.exists(os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html")):
            SearchHandler.cache_movie(url, f"~/.local/share/vidsrc-search/cache/{id}.html")
        SearchHandler.process_html(os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html"))
        print(f" • opening '{title}' in new browser tab")
        webbrowser.open("file://" + os.path.expanduser(f"~/.local/share/vidsrc-search/cache/{id}.html"))
        return

    def process_query(self) -> None:
        if len(self.query) < 1:
            return
        if self.query[0] == "'" and self.query[len(self.query) - 1] == "'":
            self.query = self.query[1:-1]
        return

    @staticmethod
    def print_warning() -> None:
        """Prints the warning before showing a movie"""
        print()
        print(" • warning: the content of the movie is hosted on a third party site. the")
        print("            site is not endorsed by the author or checked for its quality, ")
        print("            content, or authenticity. the author of vidsrc-search disclaims")
        print("            any responsibility, express or implied, of the consequences ")
        print("            as a result your usage or dependence on the website provided ")
        print("            through this tool. ")
        print(" • warning: the following window shown will be the cached contents of vidsrc.to")
        affirm = input(" > i have read and understood the conditions above (Y/n) ")
        print()
        if not affirm == "Y":
            print(" • terminating per user request")
            raise UserWarning
        return

    @staticmethod
    def cache_movie(url: str, path: str) -> None:
        """Caches a movie html to disk"""
        response = requests.get(url)
        LogSearch.log(f"caching movie from '{url}'")
        LogSearch.log(f"remote html response status code is {response.status_code}")
        with open(os.path.expanduser(path), "w") as f:
            f.write(response.content.decode())

    @staticmethod
    def delete_substring(text, start_offset, end_offset):
        """Delete a section of the text from a start offset to an end offset"""
        deleted_text = text[:start_offset - 1] + text[end_offset + 1:]
        return deleted_text

    @staticmethod
    def process_html(path):
        with open(path, "r") as f:
            content = "".join(f.readline())
            content = re.sub(r"src=(['\"])(?:(?!\\1|cloudflare|embed)[^\\'\\\"])*\\1", "src=''", content)
        with open(path, "w") as f:
            f.write(content)


def run_module(modules: List[str], args: Dict[str, Any]) -> None:
    """Runs the search module"""
    if len(modules) != 2:
        raise ArgumentsError(f"expected 1 argument for command 'search', got {len(modules) - 1} instead")
    if args["new"] and args["raw"]:
        raise ArgumentsError(f"'--new' and '--raw' are mutually exclusive flags")
    search = SearchHandler(modules[1], args)
    search.handle_search()
    return

