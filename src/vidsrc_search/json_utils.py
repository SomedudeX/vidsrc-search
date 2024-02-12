import os
import json

def load_json(path: str) -> list:
    ret: list = []
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return ret
    with open(path, "r") as f:
        ret.append(json.load(f))
        return ret
        

def parse_entry(page: dict) -> list:
    ret: list = []
    for entry in page["result"]["items"]:
        if "embed_url_imdb" in entry: 
            ret.append(entry)
    return ret


def unite_jsons(movie_index: int, tv_index: int) -> None:
    print(f" [Info] Uniting {movie_index + tv_index} json files")
    unparsed_entries = []
    parsed_entries = []
    for i in range(movie_index): 
        unparsed_entries.append(
            load_json(f"~/.config/pymovie/movie_buffer/{i}.json")
        )
    for i in range(tv_index): 
        unparsed_entries.append(
            load_json(f"~/.config/pymovie/tv_buffer/{i}.json")
        )

    print(f" [Info] Parsing {movie_index + tv_index} json files")
    for page in unparsed_entries:
        parsed_entries += parse_entry(page[0])

    print(" [Info] Dumping parsed json")
    path = os.path.expanduser("~/.config/pymovie/lib.json")
    with open(path, "w") as f:
        json.dump(parsed_entries, f, indent=4)
    return
