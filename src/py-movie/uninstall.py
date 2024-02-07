import os
import time
import shutil
import pathlib


USER_HOME_FOLDER = str(pathlib.Path.home())


def delete_directory(Path: str) -> None:
	if os.path.exists(Path):
		shutil.rmtree(Path)


def remove_file(Path: str) -> None:
	if os.path.exists(Path):
		os.remove(Path)


def uninstall():
	print(" [Log] Deleting folders...")
	time.sleep(0.1)
	delete_directory(f"{USER_HOME_FOLDER}/.config/pymovie/buffer")

	remove_file(f"{USER_HOME_FOLDER}/.config/pymovie/settings.json")
	remove_file(f"{USER_HOME_FOLDER}/.config/pymovie/lib.json")
	print(" [Log] Succesfully removed all traces from system")
	print(" [Log] If you wish to uninstall, delete this folder. Otherwise, run entrypoint.py for a clean boot")
	print(" [Log] Exiting...")
