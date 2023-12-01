from sys import platform
from time import sleep as wait
from sys import exit as terminate
from os import system as shell_command
from bootstrapper import initialize as init_bootstrapper
from multiprocessing import freeze_support as fix_pyinstaller_multiprocessing_issue
from colorama import just_fix_windows_console as fix_windows_color_output


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

	if platform == "win32":
		shell_command("cls")
	else: 
		shell_command("clear")


if __name__ == "__main__": 
	fix_windows_color_output()
	fix_pyinstaller_multiprocessing_issue()
	clear()
	print(f"{COLOR.BOLD}\b [Log] Initializing bootstrapper{COLOR.END}")
	try: wait(0.5)
	except: pass
	init_bootstrapper()

	from main import mainloop
	print(f"{COLOR.BOLD}\b [Log] Entering mainloop{COLOR.END}")
	try: wait(0.2)
	except: pass
	try: mainloop()
	except: pass
	clear()
	print(" [Log] Terminated by user request...")
	print(" [Log] Finishing script...")
	wait(0.2)
	terminate(0)
