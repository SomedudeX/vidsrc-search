import os
import sys
import json
import time
import pathlib
import download_engine


class COLOR:
	if sys.platform == "win32": 
		PURPLE = ''
		CYAN = ''
		DARKCYAN = ''
		BLUE = ''
		GREEN = ''
		YELLOW = ''
		RED = ''
		BOLD = ''
		UNDERLINE = ''
		END = ''
	else: 
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


def make_directory(Path: str) -> None:
	if os.path.exists(Path):
		return
	os.makedirs(Path)


def make_file(Path: str) -> None:
	if os.path.exists(Path):
		return
	open(Path, "x")


def initial_boot() -> None:
	print()
	print(" > Welcome to PyMovie (Terminal Edition)")
	print(" > The following script will automatically download libraries and configure PyMovie for usage")
	print(" > This process may take some time")
	print(" > ")
	input(" > Press [Enter/Return] to continue... ")
	print()
	time.sleep(0.5)

	USER_HOME_FOLDER = str(pathlib.Path.home())

	print(" [Log] Writing folders...")
	time.sleep(0.1)
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie")
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv")
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/episode")

	make_file(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json")

	print(" [Log] Writing settings...")
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "w") as s:
		preset_settings = {
		    "downloaded_lib": False,
		}

		s.write(json.dumps(preset_settings, indent=4))

	time.sleep(0.1)
	download_engine.download_lib()

