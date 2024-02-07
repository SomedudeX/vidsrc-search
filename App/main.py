r"""
The main loop of the PyMovie program
"""

import os
import sys
import pathlib
import uninstall
import webbrowser
import search_engine

from imdb import Cinemagoer


# Constants
USER_HOME_FOLDER = str(pathlib.Path.home())
LOG_FILE         = f"{USER_HOME_FOLDER}/.config/pymovie/log.txt"
LIB_FILE         = f"{USER_HOME_FOLDER}/.config/pymovie/lib.json"
SETTINGS_FILE    = f"{USER_HOME_FOLDER}/.config/pymovie/settings.json"


class COLOR:
	PURPLE = '\033[95m\b'
	CYAN = '\033[96m\b'
	DARKCYAN = '\033[36m\b'
	BLUE = '\033[94m\b'
	GREEN = '\033[92m\b'
	YELLOW = '\033[93m\b'
	RED = '\033[91m\b'
	BOLD = '\033[1m\b'
	UNDERLINE = '\033[4m\b'
	END = '\033[0m\b'


HELP_MSG = f"{COLOR.BOLD}                                                            \n\
 > Help                                                                              \n\
 > These commands are universally available in every input field in this application \n\
 >                                                                                   \n\
 > '-h', '--help'                    Displays this panel                             \n\
 > '-a', '--acknowledgements'        Displays acknowledgements page                  \n\
 > '-q', '--quit'                    Quits the application                           \n\
 > '-r', '--reset'                   Remove all traces of the application and resets \n\
 >                                   PyMovie to its original settings. Does not      \n\
 >                                   remove the application bundle/script itself     \n\
 >                                                                                   \n\
 > In addition, submitting nothing to an input field (i.e. pressing [Return/Enter]   \n\
 > in an input field) will result in going back up a page. If the PyMovie is already \n\
 > in the topmost page, it will quit instead.                                        \n\
 >                                                                                   \n\
 > Additionally, using [Ctrl+C] will force-quit PyMovie under any circumstance       \n\
 {COLOR.END}                                                                         \n"

SEARCH_MOVIE_MSG = f"{COLOR.BOLD} > Search movies:  {COLOR.END}"


def show_acknowledgements() -> None:
	webbrowser.open("https://github.com/SomedudeX/PyMovie/blob/main/Acknowledgements.md")
	clear()


def clear():
	if sys.platform == "win32":
		os.system("cls")
	else: 
		os.system("clear")


def show_help() -> None:
	clear()
	print(HELP_MSG)
	input(" > Press [Enter/Return] to continue...")
	clear()


def get_movie(MovieID): 
	ia = Cinemagoer()
	MovieID = MovieID.replace("t", "")
	Movie = ia.get_movie(MovieID)
	return Movie


def show_uninstall_message() -> None:
	print()
	Affirm = input(f"{COLOR.RED}{COLOR.BOLD}\b\b > Are you sure you want to reset this program? (Y/n) {COLOR.END}")
	if Affirm == "Y":
		uninstall.uninstall()
		print(" [Log] Program succesfully reset")
		input(" [Log] Press [Return/Enter] to quit ")
		sys.exit(0)


def parse_query(query):
	if query == "":
		return "back"

	try:
		query = int(query)
		return query
	except ValueError: pass

	try: 
		if query[0] == "-" and query[1] == "-":
			return query.replace("-", "", 2)
		if query[0] == "-":
			return query.replace("-", "", 1)
	except IndexError: pass

	return "continue"


def show_searched_movies(Entries):
	clear()
	for index, value in enumerate(reversed(Entries), start=1):
		print(f" \n\
{COLOR.BOLD}{len(Entries)-index+1}. {value['Title']}){COLOR.END}\n\
 > Type   : {value['Type'].capitalize()}                        \n\
 > Match  : {round(value['Match'], 1)}%                         \n\
 > IMDB ID: {value['ID']}                                       \n")
	print()


def show_entry(Entries, Action) -> None:
	clear()
	print(f" {COLOR.BOLD}{Action}. {Entries[Action-1]['Title']}{COLOR.END}")
	print(f" > Type   : {Entries[Action-1]['Type'].capitalize()}")
	print(f" > Match  : {round(Entries[Action-1]['Match'], 1)}%")
	print(f" > IMDB ID: {Entries[Action-1]['ID'].replace('t', '')}")
	print()
	print(COLOR.BOLD, "\b > ==== Selected entry ====", COLOR.END)
	print()
	print(" > Available actions: ")
	print(" > [1] Watch the entry in your browser      [2] Get more info on entry\n > [Return/Enter] Back a level")


def show_unexpected_command(Command) -> None:
	clear()
	print(f"{COLOR.RED}{COLOR.BOLD} [Error] Unexpected command entered ({Command})     \n\
 > Please enter a valid command. A list of commands are available via '-h' or '--help' \n\
 >                                                                                       ")
	input(f" > Press [Return/Enter] to continue... {COLOR.END}")
	clear()


def show_entry_page(Entries, Action): 
	Subaction = input(" > Action: ")
	Subaction = parse_query(Subaction)
	if Subaction == 1:
		webbrowser.open(Entries[Action-1]['URL'])
	elif Subaction == 2:
		print()
		print(" [Log] Getting infoset... (This could take a while) ")
		Movie = get_movie(Entries[Action-1]['ID'])
		clear()
		print(f" {COLOR.BOLD}{Action}. {Entries[Action-1]['Title']}{COLOR.END}")
		if "genres" in Movie: 
			print(f" > Type   : {Entries[Action-1]['Type'].capitalize()} ({Movie['genres'][0]})")
		else: 
			print(f" > Type   : {Entries[Action-1]['Type'].capitalize()}")
		if "runtimes" in Movie: 
			print(f" > Runtime: {Movie['runtimes'][0]} minutes")
		else: 
			print(f" > Runtime: Undetermined")
		print(f" > IMDB ID: {Entries[Action-1]['ID']}")
		if "plot" in Movie: 
			print()
			print(f"{COLOR.BOLD} Synopsis - {COLOR.END}")
			print(Movie["plot"][0])
		if "directors" in Movie: 
			print()
			print(f"{COLOR.BOLD} Director(s) - {COLOR.END}")
			Directors = ""
			for director in Movie['directors']:
				Directors = Directors + director['name'] + ", "
			print(f"{Directors[:-2]}")
		if "cast" in Movie: 
			print()
			print(f"{COLOR.BOLD} Cast(s) - {COLOR.END}")
			Casts = ""
			for cast in Movie['cast']:
				Casts = Casts + cast['name'] + ", "
			print()
			print(f"{Casts[:-2]}")
		if "synopsis" in Movie: 
			print()
			print(f"{COLOR.BOLD} Plot (Spoilers) - {COLOR.END}")
			print()
			print(Movie["synopsis"][0])
		print()
		print(COLOR.BOLD, "\b > ==== Entry details ====", COLOR.END)
		print()
		print(" > Available actions: ")
		print(" > [1] Watch in browser                     [Return/Enter] Back a level")
		Subaction = input(" > Action: ")
		Subaction = parse_query(Subaction)
		if Subaction == "W" or Subaction == "w":
			webbrowser.open(Entries[Action-1]['URL'])
		else: 
			if Subaction == "continue": 
				return "continue"
			elif Subaction == "settings" or Subaction == "s":
				show_settings()
				return "continue"
			elif Subaction == "acknowledgements" or Subaction == "a":
				show_acknowledgements()
				return "continue"
			elif Subaction == "help" or Subaction == "h":
				show_help()
				return "continue"
			elif Subaction == "quit" or Subaction == "q":
				return "quit"
			elif Subaction == "reset" or Subaction == "r":
				show_uninstall_message()
				return "continue"
			elif Subaction == "back":
				return "continue"
			else:
				show_unexpected_command(Subaction)
				return "continue"
	else:
		if Subaction == "continue": 
			return "continue"
		elif Subaction == "settings" or Subaction == "s":
			show_settings()
			return "continue"
		elif Subaction == "acknowledgements" or Subaction == "a":
			show_acknowledgements()
			return "continue"
		elif Subaction == "help" or Subaction == "h":
			show_help()
			return "continue"
		elif Subaction == "quit" or Subaction == "q":
			return "quit"
		elif Subaction == "reset" or Subaction == "r":
			show_uninstall_message()
			return "continue"
		elif Subaction == "back":
			return "continue"
		else:
			show_unexpected_command(Subaction)
			return "continue"


def show_movies_page(Entries, Query):
	while True: 
		clear()
		show_searched_movies(Entries)
		print(COLOR.BOLD, f"\b > ==== Search results for '{Query}' ====", COLOR.END)
		print(f"[1 - {len(Entries)}] Choose an entry        [Return/Enter] Back a level")
		Action = input(" > Action: ")

		Action = parse_query(Action)
		if type(Action) is int:
			try:
				Entries[Action-1]
			except:
				continue
			else:
				show_entry(Entries, Action)
				Action = show_entry_page(Entries, Action)
		
		if Action == "continue": 
			continue
		elif Action == "settings" or Action == "s":
			show_settings()
			continue
		elif Action == "acknowledgements" or Action == "a":
			show_acknowledgements()
			continue
		elif Action == "help" or Action == "h":
			show_help()
			continue
		elif Action == "quit" or Action == "q":
			return "quit"
		elif Action == "reset" or Action == "r":
			show_uninstall_message()
			return "continue"
		elif Action == "back":
			return "continue"
		else:
			show_unexpected_command(Action)
			continue


def mainloop(): 
	Query = input(SEARCH_MOVIE_MSG)
	Action = parse_query(Query)

	if Action == "continue":
		Entries = search_engine.SearchLibrary(Query)
		Action = show_movies_page(Entries, Query)
	elif Action == "settings" or Action == "s":
		show_settings()
		return 0
	elif Action == "acknowledgements" or Action == "a":
		show_acknowledgements()
		return 0
	elif Action == "help" or Action == "h":
		show_help()
		return 0
	elif Action == "reset" or Action == "r":
		show_uninstall_message()
		return "continue"
	elif Action == "quit" or Action == "q":
		return 1
	elif Action == "back":
		return 1
	else:
		show_unexpected_command(Action)
		return 0


	if Action == "continue":
		clear()
		return 0
	if Action == "quit" or Action == "q":
		return 1
	elif Action == "back":
		return 1
	else:
		show_unexpected_command(Action)
		clear()
		return 0

