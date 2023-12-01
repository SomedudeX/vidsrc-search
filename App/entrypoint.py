import os
import sys
import time
import bootstrapper


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


def clear():

	if sys.platform == "win32":
		os.system("cls")
	else: 
		os.system("clear")


if __name__ == "__main__": 
	print(f"{COLOR.BOLD}\b [Log] Initializing bootstrapper{COLOR.END}")
	time.sleep(0.5)
	bootstrapper.initialize()
	print(f"{COLOR.BOLD}\b [Log] Entering mainloop{COLOR.END}")
	import main
	time.sleep(0.2)
	main.mainloop()
	print(" [Log] Aborted by user request...")
	time.sleep(0.2)