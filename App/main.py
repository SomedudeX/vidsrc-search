import os
import sys
import time
import uninstall
import webbrowser
import search_engine

from imdb import Cinemagoer


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


def get_movie(MovieID) -> None: 
	ia = Cinemagoer()
	MovieID = MovieID.replace("t", "")
	Movie = ia.get_movie(MovieID)
	return Movie


def mainloop(): 
	while True: 
		while True: 
			clear()
			Query = input(f"{COLOR.BOLD} > Search movies: {COLOR.END}")
			if Query == "":
				return
			clear()
			Entries = search_engine.search_library(Query)
			if Entries == None:
				break
			for index, value in enumerate(reversed(Entries), start=1):
				print()
				print(f" {COLOR.BOLD}{len(Entries)-index+1}. {value['Title']}{COLOR.END}")
				print(f" > Type   : {value['Type'].capitalize()}")
				print(f" > Match  : {round(value['Match'], 1)}%")
				print(f" > IMDB ID: {value['ID']}")
			print()
			print(COLOR.BOLD, f"\b > ==== Search results for '{Query}' ====", COLOR.END)
			print()
			print(" > Available actions: ")
			print(" > # - Select an entry         R - Reset Application")
			Action = input(" > Action: ")
			try:
				Action = int(Action)
				Entries[Action-1]
			except:
				if Action == "R" or Action == "r":
					Affirm = input(f"{COLOR.RED}{COLOR.BOLD}\b\b > Are you sure you want to reset this program? (Y/n) {COLOR.END}")
					if Affirm == "Y":
						uninstall.uninstall()
						print(" [Log] Program succesfully reset: Quitting...")
						time.sleep(1)
						sys.exit(0)
				else: 
					break
			else: 
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
				Subaction = input(" > Subaction: ")
				if Subaction == "W" or Subaction == "w":
					webbrowser.open(Entries[Action-1]['URL'])
				if Subaction == "I" or Subaction == "i":
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
					if Subaction == "W" or Subaction == "w":
						webbrowser.open(Entries[Action-1]['URL'])
					else: 
						break
				else:
					break

