import json
import pathlib
from thefuzz.fuzz import partial_ratio, ratio


USER_HOME_FOLDER = str(pathlib.Path.home())
LIB_FILE         = f"{USER_HOME_FOLDER}/.config/pymovie/lib.json"


def SimilarityScore(Str1: str, Str2: str) -> float:
	return (5 * partial_ratio(Str1, Str2) + ratio(Str1, Str2)) / 6


def RelevanceKey(Entry) -> float:
	return Entry["Match"]


def SortResults(Result: list) -> list:
	Result.sort(key = RelevanceKey, reverse = True)
	return Result


def SearchLibrary(Query: str) -> list | None:
	Result = []

	with open(LIB_FILE, "r") as f: MovieLib = f.read()
	MovieLib = json.loads(MovieLib) 

	for Entry in MovieLib: 
		if SimilarityScore(Entry["Title"], Query) >= 60:
			Result.append({
			"Title": Entry["Title"], 
			"ID": Entry["ID"], 
			"Type": Entry["Type"], 
			"URL": Entry["URL"], 
			"Match": SimilarityScore(Entry["Title"], Query),
			})

	if len(Result) == 0: return None
	Result = SortResults(Result)

	while len(Result) > 20: del Result[len(Result) - 1]
	return Result

