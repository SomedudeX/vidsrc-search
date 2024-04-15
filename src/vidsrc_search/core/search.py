# Using classes for better organization

import os
import json
import requests
import webbrowser

from .. import utils
from ..argparsing import ArgumentsError
from .library import Library

from typing import Any, Dict, List, Tuple, Union

from tabulate import tabulate
from thefuzz.fuzz import partial_ratio, ratio
from html.parser import HTMLParser


class FileProcessor(HTMLParser):
    """Processes the HTML file downloaded from vidsrc.to. This class is derived
    from the HTMLParser class in Python's standard library. See its
    documentation for more information.

    When calling the feed() function on an instance of this class, it will mark
    any start and end tag that is "bad" (aka an ad/redirect script) and store
    it in the class attributes.
    """

    def __init__(self) -> None:
        """Initializes a FileProcessor and its parent class"""
        self.start_positions: List[Tuple] = []  # bad start tags
        self.end_positions: List[Tuple] = []    # bad end tags
        self.positions_tag: List[str] = []      # type of tag

        self._current_bad_script = 0
        self._current_bad_element = 0
        super().__init__()
        return

    def handle_starttag(
        self,
        tag: Union[str, Any],
        attrs: List[Any]
    ) -> None:
        """When a start tag is encountered, this function is automatically
        called. It will insert the current position (lineno and offset) to
        the start_positions if the tag is "bad"
        """
        if tag not in ["script"]:
            return
        for attr in attrs:
            if self.bad_script(attr):
                self._current_bad_script += 1
                self.start_positions.append(self.getpos())
        return

    def handle_endtag(
        self,
        tag: Union[str, Any]
    ) -> None:
        """When an end tag is encountered, this function is automatically
        called. It will insert the current position (lineno and offset) to
        the end_positions if the tag is "bad"
        """
        if tag not in ["script"]:
            return
        if self._current_bad_script == 1:
            self._current_bad_script = 0
            self.end_positions.append(self.getpos())
            self.positions_tag.append("</script>")
        if self._current_bad_script != 0:
            self._current_bad_script -= 1
        return

    @staticmethod
    def bad_script(script_attr: tuple):
        """Checks if a scrip attribute is a "bad" attribute"""
        if script_attr[0] != "src":
            return False
        if "embed" in script_attr[1]:
            return False
        if "cloudflare" in script_attr[1]:
            return False
        return True


class SearchManager:
    """Library search related functions"""

    def __init__(
        self,
        query: str
    ) -> None:
        """Initializes a SearchManager object with a query"""
        self.query: str = query
        self.results: List[Dict] = []
        return

    def search_library(self) -> None:
        """Initiates a library search with the query specified during init"""
        library = Library()
        library.check_library()
        with open(library.lib_path, "r") as f:
            library = f.read()
        library = json.loads(library)

        for entry in library:
            self.check_entry(entry)
        self.sort_results()

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

        self.raw = args["raw"]
        self.new = args["new"]
        return

    def begin_search(self) -> None:
        """Handles searching the movie library"""
        self.process_query()
        print(f"info: searching json library for '{self.query}'")
        print(f"info: open raw website: {str(self.raw).lower()}")
        print(f"info: recaching website: {str(self.new).lower()}")
        self.manager = SearchManager(self.query)
        self.manager.search_library()
        self.results = self.manager.results
        if len(self.results) == 0 :
            print(f"info: '{self.query}' not found in movies library")
            print(f"info: vidsrc-search terminating due to entry not found")
            return
        self.print_movies()
        open_index = self.ask_open_index()
        self.show_movie(open_index)
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
                print("error: please enter a valid value")
                continue

    def show_movie(self, index: int) -> None:
        """Shows the movie chosen by the user in their browser"""
        SearchHandler.print_warning()
        utils.check_internet()

        number = index + 1
        title = self.results[index]["Title"]
        url = self.results[index]["URL"]
        id = self.results[index]["IMDB ID"]

        if self.raw:
            print(f"info: opening #{number} '{title}' in new browser window")
            webbrowser.open(url)
            return

        if self.new or not os.path.exists(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html")):
            SearchHandler.cache_movie(url, f"~/.local/vidsrc-search/cache/{id}.html")
        SearchHandler.process_html(os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"))
        print(f"info: opening #{number} '{title}' in new browser window")
        webbrowser.open("file://" + os.path.expanduser(f"~/.local/vidsrc-search/cache/{id}.html"))
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
        print("warning: the content of the movie is hosted on a third party site. the")
        print("         site is not endorsed by the author or checked for its quality, ")
        print("         content, or authenticity. the author of vidsrc-search disclaims")
        print("         any responsibility, express or implied, of the consequences ")
        print("         as a result your usage or dependence on the website provided ")
        print("         through this tool. ")
        print("warning: the following window shown will be the cached contents of vidsrc.to\n")
        affirm = input(" > i have read and understood the conditions above (Y/n) ")
        print()
        if not affirm == "Y":
            print("info: terminating per user request")
            raise UserWarning
        return

    @staticmethod
    def cache_movie(url: str, path: str) -> None:
        """Caches a movie html to disk"""
        response = requests.get(url)
        print(f"info: caching movie from remote html")
        print(f"info: remote html request status code is {response.status_code}")
        with open(os.path.expanduser(path), "w") as f:
            f.write(response.content.decode())
            print(f"info: finished caching html")

    @staticmethod
    def delete_substring(text, start_offset, end_offset):
        """Delete a section of the text from a start offset to an end offset"""
        deleted_text = text[:start_offset - 1] + text[end_offset + 1:]
        return deleted_text

    @staticmethod
    def process_html(path: str) -> None:
        """Processes the html file downloaded from vidsrc.to"""
        print(f"info: processing html")
        with open(path, "r") as f:
            content = f.readlines()
            content = ''.join(content)
            while True:
                parser = FileProcessor()
                parser.feed(content)
                if len(parser.positions_tag) == 0:
                    break
                content = SearchHandler.delete_substring(
                    content,
                    parser.start_positions[0][1] + 1,
                    parser.end_positions[0][1] + len(parser.positions_tag[0]) - 1
                )

        print(f"info: writing processed html")
        with open(path, "w") as f:
            f.write(content)


def run_module(modules: List[str], args: Dict[str, Any]) -> None:
    """Runs the search module"""
    if len(modules) != 2:
        raise ArgumentsError(f"expected 1 argument for command 'search', got {len(modules) - 1} instead")
    if args["new"] and args["raw"]:
        raise ArgumentsError(f"'--new' and '--raw' are mutually exclusive flags")
    search = SearchHandler(modules[1], args)
    search.begin_search()
    return

