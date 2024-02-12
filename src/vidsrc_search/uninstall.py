import os
import sys
import json


def handle_remove() -> None:
    lib_path = os.path.expanduser("~/.config/pymovie/lib.json")
    if not os.path.exists(lib_path):
        print(" [Fatal] Library does not exist")
        print(" [Fatal] Please download the library first by using 'vidsrc-search libary download'")
        print(" [Fatal] Vidsrc-search terminating with exit code 2")
        sys.exit(2)
    with open(lib_path, "r") as f:
        jsons = json.load(f)
        
    confirm = input(f" > Are you sure you want to remove ~{len(jsons) * 15} links to movies? (Y/n) ")
    if not confirm == "Y":
        print(" [Info] User declined operation")
        print(" [Info] Vidsrc-search terminating per user request")
        sys.exit(0)
    
    print(" [Info] Removing library json file")
    os.remove(lib_path)
    print(" [Info] Library json file removed")
    return       
