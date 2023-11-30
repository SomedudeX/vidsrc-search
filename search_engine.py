import json
import requests
import pathlib
from thefuzz import fuzz
from imdb import Cinemagoer


USER_HOME_FOLDER = str(pathlib.Path.home())
LIB_FILE = f"{USER_HOME_FOLDER}/.config/pymovie/lib.json"


def similarity_score(str1: str, str2: str) -> int:
	return (5 * fuzz.partial_ratio(str1, str2) + fuzz.ratio(str1, str2)) / 6


def relevance_key(a):
	return a["Match"]



def sort_results(Result: list) -> list:
	Result.sort(key=relevance_key, reverse=True)
	return Result


def search_library(Query: str) -> list:
	Result = []

	with open(LIB_FILE, "r") as f:
		MovieLib = f.read()
	MovieLib = json.loads(MovieLib) 

	for Entry in MovieLib: 
		if similarity_score(Entry["Title"], Query) >= 60:
			Result.append({
				"Title": Entry["Title"], 
				"ID": Entry["ID"], 
				"Type": Entry["Type"], 
				"URL": Entry["URL"], 
				"Match": similarity_score(Entry["Title"], Query),
			})

	if len(Result) == 0: 
		return None

	Result = sort_results(Result)

	while len(Result) > 20: 
		del Result[len(Result) - 1]
	
	return Result

