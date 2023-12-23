import os
import sys
import time
import json
import shutil
import pathlib
import firstboot
import download_engine


from multiprocessing import freeze_support as patch_mp_issue


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


def python_version() -> str:
	return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


def delete_directory_recursive(Path: str):
	shutil.rmtree(Path)


def make_directory(Path: str) -> None:
	if os.path.exists(Path):
		return
	os.makedirs(Path)


def load_settings() -> dict:
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "r") as s:
		return json.load(s)


def write_to_settings(settings: dict) -> None:
	with open(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json", "w") as s:
		json.dump(settings, s, indent=4)


def check_initial_boot():
	if is_first_boot():
		print(f"{COLOR.BOLD}\b [Log] Initial boot detected {COLOR.END}")
		try:
			firstboot.initial_boot()
		except KeyboardInterrupt:
			handle_keyboard_interrupt()


def clear():
	if sys.platform == "darwin":
		os.system("clear")
	else:
		os.system("cls")


def is_windows_cmd() -> bool:
	import psutil
	TerminalPID = os.getppid()
	TerminalType = psutil.Process(TerminalPID).name()
	if TerminalType == "cmd.exe":
		return True
	return False


def check_required_libraries() -> None:
	try:
		import thefuzz
		import imdb
		import requests
		import psutil
		import colorama
	except ImportError as e:
		print()
		print(f"{COLOR.BOLD}{COLOR.RED}\b [Error] Required package not installed: {str(e).lower()}")
		print(f" > Program cannot continue, make sure you have installed all required packages in your current python version. ({python_version()})")
		print(f" > All required packages can be installed through 'pip' (Windows) or 'pip3' (macOS/Linux) command. ")
		print(f" > ")
		input(f" > Press [Enter/Return] to quit... {COLOR.END}")
		sys.exit()


def is_first_boot() -> bool:
	if not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie"):
		return True
	if not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json"):
		return True
	if not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/lib.json"):
		return True
	if not os.path.exists(f"{USER_HOME_FOLDER}/.config/pymovie/buffer"):
		return True
	return False


def handle_keyboard_interrupt() -> None:
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
	sys.exit()


def initialize():
	print(" [Log] Checking for required libraries... ")
	check_required_libraries()

	from colorama import just_fix_windows_console as patch_win_console
	print(" [Log] Applying patches")
	patch_mp_issue()
	patch_win_console()

	print(" [Log] Checking for initial boot... ")
	check_initial_boot()

	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/movie")
	make_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer/tv")

	Settingsfile = load_settings()

	print(" [Log] Checking shell type...")
	if is_windows_cmd() and Settingsfile["supress_startup_warning"] == False:
		print()
		print(f"{COLOR.YELLOW}\b [Warning] Running this program in Windows cmd could result in unexpected behavior")
		print(f" > Consider using Windows Powershell instead")
		print(f" > ")
		Supress_Warning = input(f" > Press [Shift+S+Enter] to supress this warning, or [Enter/Return] to continue...{COLOR.END}")
		print()
		if Supress_Warning == "S":
			Settingsfile["supress_startup_warning"] == True
			write_to_settings(Settingsfile)

	print(" [Log] Verifying library...")
	if Settingsfile["downloaded_lib"] == False:
		print(f"{COLOR.RED}\b [Log] Library not detected... {COLOR.END}")
		print(f"{COLOR.BOLD}\b [Log] Downloading Library (this may take a while){COLOR.END}...")
		try:
			download_engine.download_lib()
		except KeyboardInterrupt:
			handle_keyboard_interrupt()

	print(f"{COLOR.GREEN}{COLOR.BOLD}\b\b [Log] Bootstrapper finished", COLOR.END)
