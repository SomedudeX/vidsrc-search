#!/usr/bin/env python3
import os
import sys
import time
import bootstrapper

from multiprocessing import freeze_support as patch_mp


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


def clear():
	if sys.platform == "win32":
		os.system("cls")
	else: 
		os.system("clear")


def do_mainloop():
	import main
	clear()
	print(f" > PyMovie succesfully launched with Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
	print(f" > Type [Return/Enter] to exit PyMovie or go back up a page")
	print(f" > Type '-h' or '--help' for help page")
	print(f" > ")
	while True:
		if main.mainloop() == 1:
			break


def print_exit_msg():
	clear()
	print(" [Log] Terminated per user request...")
	print(" [Log] Finishing script...")
	if sys.platform == "win32":
		print()
		input(" > Press [Return/Enter] to quit...")


def pymovie():
	try: 
		patch_mp()
		clear()
		print(" [Log] Initializing bootstrapper")
		bootstrapper.initialize()

		print(" [Log] Entering mainloop")
		do_mainloop()
		print_exit_msg()
		sys.exit(0)
	except KeyboardInterrupt:
		try:
			print()
		except KeyboardInterrupt:
			pass
		print_exit_msg()
	except Exception as e:
		print(f" [Log] An exception occured during the execution of PyMovie")
		print(f" [Log] Exception message: {str(e).lower()}")
		print(f" [Log] Terminating script...")

