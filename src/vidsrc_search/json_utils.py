import os
import json


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
    print(f" [Info] Uniting {movie_index + tv_index} json files")
    unparsed_entries = []
    parsed_entries = []
    for i in range(movie_index): 
        unparsed_entries.append(load_json(f"~/.local/vidsrc-search/movie_buffer/{i}.json"))
    for i in range(tv_index): 
        unparsed_entries.append(load_json(f"~/.local/vidsrc-search/tv_buffer/{i}.json"))

    print(f" [Info] Parsing {movie_index + tv_index} json files")
    for page in unparsed_entries:
        parsed_entries += parse_entry(page[0])

    print(" [Info] Dumping parsed json")
    path = os.path.expanduser("~/.local/vidsrc-search/lib.json")
    with open(path, "w") as f:
        json.dump(parsed_entries, f)
    return len(parsed_entries)
