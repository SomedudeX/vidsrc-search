import os
import sys
import json
import time
import pathlib
import requests

from multiprocessing import Process
from shutil import rmtree


USER_HOME_FOLDER = str(pathlib.Path.home())


class COLOR:
	PURPLE = '\033[95m'
	CYAN = '\033[96m'
	DARKCYAN = '\033[36m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	END = '\033[0m'


def delete_directory_recursive(Path: str):
	rmtree(Path)

def is_multiple_of_96(Index: int) -> bool:
	if Index % 96 != 0:
		return False
	if Index == 0:
		return False
	return True


def add_process(Processes: list, Index: int, Type: str) -> list:
	Processes.append(Process(target=request_downloads, args=(Index, Type)))
	Processes[Index].start()
	return Processes


def clean_up_processes(Processes: list, Index: int) -> list:
	for i in range(Index-97, Index): 
		try: 
			Processes[i].join()
			Processes[i].close()
		except ValueError: 
			pass

def check_download_finish(DESTINATION_URL: str, Index: int) -> bool:
	if len(requests.get(f"{DESTINATION_URL}/{Index}").content) < 50:
		return True
	return False


def get_folder_size(Path: str):
	Size = 0
	for path, dirs, files in os.walk(Path):
		for f in files:
			Fp = os.path.join(path, f)
			Size += os.path.getsize(Fp)
	return round(Size/1000000, 2)
			

def parse_entry(Entry: dict) -> dict: 
	ParsedEntry = {
		"Title": Entry["title"], 
		"Type": Entry["type"], 
		"URL": Entry["embed_url_imdb"], 
		"ID": Entry["imdb_id"],
	}

	if "season" in Entry: 
		Season = Entry["season"]
	if "number" in Entry: 
		Episode = Entry["number"]

	return ParsedEntry


def request_downloads(Index: int, Type: str) -> None: 
	USER_HOME_FOLDER = str(pathlib.Path.home())
	DOWNLOAD_PATH = f"{USER_HOME_FOLDER}/.config/pymovie/buffer/{Type}/{Index}.json"

	if Type == "episode":
		Url = f"https://vidsrc.to/vapi/{Type}/latest/{Index}"
		File = requests.get(Url)
	else: 
		Url = f"https://vidsrc.to/vapi/{Type}/new/{Index}"
		File = requests.get(Url)

	if len(File.content) < 50: 
		return
	with open(DOWNLOAD_PATH, "wb") as f: 
		f.write(File.content)


def download_movies() -> int:
	print(" [Log] Started downloading movies... (Step 1/4)")
	DESTINATION_URL = "https://vidsrc.to/vapi/movie/new"
	Processes = []
	Index = 0

	while True: 
		if is_multiple_of_96(Index): 
			print(f" [Log] Cleanup #{int(Index/96)} ({round(100*(Index/2550), 2)}%)")
			clean_up_processes(Processes, Index)
			if check_download_finish(DESTINATION_URL, Index):
				break
		Processes = add_process(Processes, Index, "movie")
		Index += 1

	print(f" [Log] Movies succesfully downloaded ({Index + 1})")
	return Index


def download_tv() -> int:
	print(" [Log] Started downloading tv... (Step 2/4)")
	DESTINATION_URL = "https://vidsrc.to/vapi/tv/new"
	Processes = []
	Index = 0

	while True: 
		if is_multiple_of_96(Index): 
			print(f" [Log] Cleanup #{int(Index/96)} ({round(100*(Index/850), 2)}%)")
			clean_up_processes(Processes, Index)
			if check_download_finish(DESTINATION_URL, Index):
				break
		Processes = add_process(Processes, Index, "tv")
		Index += 1

	print(f" [Log] TV succesfully downloaded ({Index + 1})")
	return Index


# def download_episodes() -> int:
# 	print("Started downloading episodes... (Step 3/5)")
# 	DESTINATION_URL = "https://vidsrc.to/vapi/episode/latest"
# 	Processes = []
# 	Index = 0

# 	while True: 
# 		if is_multiple_of_96(Index): 
# 			print(f" > Cleanup #{int(Index/96)} ({round(100*(Index/2304), 2)}%)")
# 			clean_up_processes(Processes, Index)
# 			if Index == 2304:
# 				break
# 		Processes = add_process(Processes, Index, "episode")
# 		Index += 1

# 	print(f"Episodes succesfully downloaded ({Index + 1})")
# 	return Index


def unite_jsons(MovieIndex: int, TVIndex: int) -> None:
	print(" [Log] Uniting jsons... (Step 3/4)")
	UnparsedEntries = []
	ParsedEntries = []
	for i in range(MovieIndex): 
		try: 
			with open(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie/{i}.json", "r") as Json1:
				UnparsedEntries.append(json.loads(Json1.read()))
		except:
			pass
	for i in range(TVIndex-2): 
		try:
			with open(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv/{i}.json", "r") as Json2:
				UnparsedEntries.append(json.loads(Json2.read()))
		except:
			pass

	print(" [Log] Parsing each entry...")
	for page in range(len(UnparsedEntries)):
		for index, entry in enumerate(UnparsedEntries[page]["result"]["items"]):
			if "embed_url_imdb" in entry: 
				ParsedEntries.append(parse_entry(entry))

	print(" [Log] Dumping parsed json...")
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/lib.json", "w") as f:
		json.dump(ParsedEntries, f, indent=4)


def download_lib() -> None:

	StartTime = time.time()
	MovieIndex = download_movies()
	TVIndex = download_tv()
	print(f"{COLOR.GREEN}{COLOR.BOLD}\b\b [Log] Download complete {COLOR.END}")

	unite_jsons(MovieIndex, TVIndex)

	print(" [Log] Writing to settings... (Step 5/5)")
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "r") as s: 
		Settings = json.loads(s.read())
		Settings["downloaded_lib"] = True

	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "w") as s:
		json.dump(Settings, s, indent=4)
	print(" [Log] Cleaning up...")
	delete_directory_recursive(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie")
	delete_directory_recursive(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv")
	EndTime = time.time()

	print(f"{COLOR.BOLD}{COLOR.GREEN}\b [Log] Succesfully downloaded library{COLOR.END}")
	print(f"{COLOR.BOLD}\b > Took {round(EndTime-StartTime, 1)}s")
	print(f" > Took {get_folder_size(f'{USER_HOME_FOLDER}/.config/pymovie')}mb of space")
	print()
	input(" > Press [Enter/Return] to continue...")
