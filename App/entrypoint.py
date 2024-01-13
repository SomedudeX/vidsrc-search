import os
import sys
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


if __name__ == "__main__": 
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
		print_exit_msg()

