import os
import sys
import time
import shutil
import pathlib
import contextlib


USER_HOME_FOLDER = str(pathlib.Path.home())


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


def delete_directory_recursive(Path: str):
	shutil.rmtree(Path)


def make_directory(Path: str) -> None:
	if os.path.exists(Path):
		return
	os.makedirs(Path)


def clear():

	if sys.platform == "darwin":
		os.system("clear")
	else: 
		os.system("cls")


def initialize(): 
	try:
		print(" [Log] Checking for required libraries... ")
		import thefuzz
		import imdb
		import requests
	except ImportError as e:
		print()
		print(f"{COLOR.BOLD}{COLOR.RED}\b [Error] Required package not installed: {str(e).lower()}")
		print(f" > Program cannot continue, make sure you have installed all required packages in your current python version. ({sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro})")
		print(f" > All required packages can be installed through 'pip' (Windows) or 'pip3' (macOS/Linux) command. ")
		print(f" > ")
		input(f" > Press [Enter/Return] to quit... {COLOR.END}")
		sys.exit(0)


	print(" [Log] Checking for initial boot... ")
	import os
	import json
	import firstboot
	import download_engine
	if not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie") or not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json") or not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/lib.json") or not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/buffer"):
		print(f"{COLOR.BOLD}\b [Log] Initial boot detected")
		try: 
			firstboot.initial_boot()
		except KeyboardInterrupt:
			time.sleep(1)
			clear()
			print(f"{COLOR.BOLD}{COLOR.RED}\b\b [Error] User terminated operation {COLOR.END}")
			print(f" [Log] Destroying cached files so as to not damage installation...")
			print(f" [Log] Files cleaned up...")
			print(f" [Log] Exiting safely...")
			print()
			if os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie"): 
				delete_directory_recursive(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie")
			if os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv"): 
				delete_directory_recursive(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv")
			sys.exit(0)
	print(" [Log] Verifying library...")
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie")
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv")
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "r") as s:
		Settingsfile = json.load(s)
		if Settingsfile["downloaded_lib"] == False:
			print(f"{COLOR.RED}\b [Log] Library not detected... {COLOR.END}")
			download_engine.download_lib()
	print(f"{COLOR.GREEN}{COLOR.BOLD}\b\b [Log] Bootstrapper finished", COLOR.END)


