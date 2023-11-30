import os
import sys
import time
import bootstrapper


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

	if sys.platform == "darwin":
		os.system("clear")
	else: 
		os.system("cls")


if __name__ == "__main__": 
	print(f"{COLOR.BOLD}\b [Log] Initializing bootstrapper{COLOR.END}")
	time.sleep(0.5)
	bootstrapper.initialize()
	print(f"{COLOR.BOLD}\b [Log] Entering mainloop{COLOR.END}")
	import main
	time.sleep(0.2)
	try: 
		main.mainloop()
	except KeyboardInterrupt:
		clear()
		print(" [Log] Terminating program...")
		time.sleep(0.2)