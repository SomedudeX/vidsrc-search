import os
import sys
import time
import uninstall
import webbrowser
import search_engine

from imdb import Cinemagoer


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


HELP_MSG = f"{COLOR.BOLD} > Help                                                     \n\
 > These commands are universally available in every input field in this application \n\
 >                                                                                   \n\
 > '-h', '--help'                    Displays this panel                             \n\
 > '-a', '--acknowledgements'        Displays acknowledgements page                  \n\
 > '-q', '--quit'                    Quits the application                           \n\
 > '-r', '--reset'                   Remove all traces of the application and resets \n\
 >                                   PyMovie to its original settings                \n\
 >                                                                                   \n\
 > In addition, submitting nothing to an input field (i.e. pressing [Return/Enter]   \n\
 > in an input field) will result in going back up a page. If the PyMovie is already \n\
 > in the topmost page, it will quit instead.                                        \n\
 >                                                                                   \n\
 > Additionally, using [Ctrl+C] will force-quit PyMovie under any circumstance       \n\
 {COLOR.END}"

SEARCH_MOVIE_MSG = f"{COLOR.BOLD} > Search movies:  {COLOR.END}"


def show_acknowledgements() -> None:
	webbrowser.open("https://github.com/SomedudeX/PyMovie/blob/main/Acknowledgements.md")


def clear():
	if sys.platform == "darwin":
		os.system("clear")
	else: 
		os.system("cls")


def get_movie(MovieID) -> None: 
	ia = Cinemagoer()
	MovieID = MovieID.replace("t", "")
	Movie = ia.get_movie(MovieID)
	return Movie


def show_uninstall_message() -> None:
	Affirm = input(f"{COLOR.RED}{COLOR.BOLD}\b\b > Are you sure you want to reset this program? (Y/n) {COLOR.END}")
	if Affirm == "Y":
		uninstall.uninstall()
		print(" [Log] Program succesfully reset: Quitting...")
		time.sleep(1)
		sys.exit(0)


def show_help() -> None:
	clear()
	print(HELP_MSG)
	input(" > Press [Enter/Return] to continue...")


def parse_query(query: str or int) -> str:
	if query == "":
		return "EXIT"
	if query == "-q" or query == "--quit":
		return "EXIT"
	if len(query) < 2:
		return "continue"
	if query[0] == "-" and query[1] == "-":
		return query.replace("-", "", 2)
	if query[0] == "-":
		return query.replace("-", "", 1)
	return "continue"


def parse_subquery(query, checkint: bool) -> str:
	if query == "W" or query == "w":
		return query
	if query == "I" or query == "i":
		return query
	try: 
		if checkint: 
			query = int(query)
			return query
	except:
		pass
	if query == "":
		return "quit"
	if query == "-q" or query == "--quit":
		return "EXIT"
	if len(query) < 2:
		return "continue"
	if query[0] == "-" and query[1] == "-":
		return query.replace("-", "", 2)
	if query[0] == "-":
		return query.replace("-", "", 1)
	return "continue"


def show_searched_movies(Entries: str) -> None:
	clear()
	for index, value in enumerate(reversed(Entries), start=1):
		print(f" \n\
{COLOR.BOLD}{len(Entries)-index+1}. {value['Title']}){COLOR.END}\n\
 > Type   : {value['Type'].capitalize()}                        \n\
 > Match  : {round(value['Match'], 1)}%                         \n\
 > IMDB ID: {value['ID']}                                       \n")
	print()


def show_entry(Entries: str, Action) -> None:
	clear()
	print(f" {COLOR.BOLD}{Action}. {Entries[Action-1]['Title']}{COLOR.END}")
	print(f" > Type   : {Entries[Action-1]['Type'].capitalize()}")
	print(f" > Match  : {round(Entries[Action-1]['Match'], 1)}%")
	print(f" > IMDB ID: {Entries[Action-1]['ID'].replace('t', '')}")
	print()
	print(COLOR.BOLD, "\b > ==== Selected entry ====", COLOR.END)
	print()
	print(" > Available subactions: ")
	print(" > W - Watch the entry in your browser      I - Get more info on entry")


def show_unexpected_command(Command) -> None:
	clear()
	print(f"{COLOR.RED}{COLOR.BOLD} [Error] Unexpected command entered \n\
 > Please enter a valid command. A list of commands are available via '-h' or '--help' \n\
 >   \n")
	input(" > Press [Return/Enter] to continue... {COLOR.END}")


def show_entry_page(Entries: str, Action: str) -> str: 
	Subaction = input(" > Subaction: ")
	Subaction = parse_subquery(Subaction, False)
	if Subaction == "W" or Subaction == "w":
		webbrowser.open(Entries[Action-1]['URL'])
	elif Subaction == "I" or Subaction == "i":
		print()
		print(" [Log] Getting infoset... (This could take a while)")
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
		print(" > Available subactions: ")
		print(" > W - Watch the entry in your browser")
		Subaction = input(" > Subaction: ")
		Subaction = parse_subquery(Subaction, False)
		if Subaction == "W" or Subaction == "w":
			webbrowser.open(Entries[Action-1]['URL'])
		else: 
			if Subaction == "acknowledgements" or Subaction == "a":
				show_acknowledgements()
				return "continue"
			elif Subaction == "help" or Subaction == "h":
				show_help()
				return "continue"
			elif Subaction == "quit" or Subaction == "q":
				return "continue"
			elif Subaction == "EXIT":
				return "EXIT"
			elif Subaction == "reset" or Subaction == "r":
				show_uninstall_message()
			elif Subaction == "continue": 
				return "continue"
			else:
				show_unexpected_command(Subaction)
	else:
		if Subaction == "acknowledgements" or Subaction == "a":
			show_acknowledgements()
			return "continue"
		elif Subaction == "help" or Subaction == "h":
			show_help()
			return "continue"
		elif Subaction == "quit" or Subaction == "q":
			return "continue"
		elif Subaction == "EXIT":
			return "EXIT"
		elif Subaction == "reset" or Subaction == "r":
			show_uninstall_message()
		elif Subaction == "continue": 
			return "continue"
		else: 
			show_unexpected_command(Subaction)



def show_movies_page(Entries: str, Query: str) -> str:
	while True: 
		clear()
		show_searched_movies(Entries)
		print(COLOR.BOLD, f"\b > ==== Search results for '{Query}' ====", COLOR.END)
		Action = input(" > Choose an entry: ")

		Action = parse_subquery(Action, True)
		if type(Action) is int:
			try:
				Entries[Action-1]
			except:
				continue
			else:
				show_entry(Entries, Action)
				Action = show_entry_page(Entries, Action)
				
		if Action == "acknowledgements" or Action == "a":
			show_acknowledgements()
			continue
		elif Action == "help" or Action == "h":
			show_help()
			continue
		elif Action == "quit" or Action == "q":
			return Action
		elif Action == "EXIT":
			return "EXIT"
		elif Action == "reset" or Action == "r":
			show_uninstall_message()
		elif Action == "continue": 
			continue
		else:
			show_unexpected_command(Action)


def mainloop(): 
	while True: 
		clear()
		Query = input(SEARCH_MOVIE_MSG)
		Action = parse_query(Query)

		if Action == "continue":
			Entries = search_engine.search_library(Query)
		elif Action == "acknowledgements" or Action == "a":
			show_acknowledgements()
			continue
		elif Action == "help" or Action == "h":
			show_help()
			continue
		elif Action == "quit" or Action == "q":
			continue
		elif Action == "reset" or Action == "r":
			show_uninstall_message()
		elif Action == "EXIT":
			break
		else:
			show_unexpected_command(Action)
		
		Action = show_movies_page(Entries, Query)

		if Action == "continue":
			continue
		if Action == "quit" or Action == "q":
			continue
		if Action == "EXIT":
			break

		

