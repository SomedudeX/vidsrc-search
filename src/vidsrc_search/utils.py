import os
import sys
import shutil
import asyncio

import requests


HELP_TEXT = ("\
Usage: vidsrc-search <command> [options]            \n\
                                                    \n\
Available commands:                                 \n\
    help        shows this menu                     \n\
    search      search a movie by name              \n\
    library     actions regarding the movie lib     \n\
                                                    \n\
Use 'vidsrc-search help <command>' for info         \n\
on a specific command.                              \
")

HELP_HELP = ("\
Usage: vidsrc-search help <option>                  \n\
                                                    \n\
Available options:                                  \n\
    help        shows detailed help for 'help'      \n\
    search      shows detailed help for 'search'    \n\
    library     shows detailed help for 'library'   \n\
                                                    \n\
Example:                                            \n\
     vidsrc-search help library                     \n\
     vidsrc-search help help                        \
")

HELP_SEARCH = ("\
Usage: vidsrc-search search <option>                \n\
                                                    \n\
Required option:                                    \n\
    <str>       a movie title that you would like   \n\
                vidsrc-search to search for         \n\
                                                    \n\
Example:                                            \n\
    vidsrc-search search 'oppenheimer'              \n\
    vidsrc-search search 'avatar'                   \
")

HELP_LIB = ("\
Usage: vidsrc-search library <option>               \n\
                                                    \n\
Required options:                                   \n\
    remove      removes the movies library          \n\
    download    downloads the latest movies library \n\
                from https://vidsrc.to              \n\
                                                    \n\
Example:                                            \n\
    vidsrc-search library download                  \
")


def show_help():
    print(HELP_TEXT)
    return


def show_help_help():
    print(HELP_HELP)
    return
    
    
def show_help_search():
    print(HELP_SEARCH)
    return
    
    
def show_help_lib():
    print(HELP_LIB)
    return


def make_directory(path: str) -> None:
    if os.path.exists(path):
        return
    os.makedirs(path)
    

def delete_directory_recursive(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)
        
        
def asyncio_patch() -> None:
    if sys.platform in ["win32", "cygwin", "msys"]:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        

def check_internet() -> None:
    print(" [Info] Verifying internet connection")
    
    try: 
        print(" [Info] Testing connection by pinging google.com")
        r = requests.get("https://google.com", allow_redirects = False)
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print() 
        print(f" [Fatal] An HTTP error was encountered")
        print(f" [Fatal] This might be due to an issue with the external server")
        print(f" [Fatal] Vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.SSLError:
        print() 
        print(f" [Fatal] Could not establish secure connection")
        print(f" [Fatal] You might be on a monitored network or using a VPN/Proxy")
        print(f" [Fatal] Vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.ConnectionError:
        print()
        print(f" [Fatal] Could not establish internet connection")
        print(f" [Fatal] Make sure you are connected to the internet")
        print(f" [Fatal] Vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.RequestException as e:
        print()
        print(f" [Fatal] An unknown network error occured: {e}")
        print(f" [Fatal] This could be due to an issue with the external server")
        print(f" [Fatal] Vidsrc-search terminating with exit code 255")
        sys.exit(255)

    try:
        print(" [Info] Testing connection by pinging vidsrc.to")
        requests.get("https://vidsrc.to", allow_redirects = False)
    except requests.exceptions.HTTPError:
        print() 
        print(f" [Fatal] An HTTP error was encountered while pinging vidsrc.to")
        print(f" [Fatal] This might be due to an issue with the external server")
        print(f" [Fatal] Vidsrc-search terminating with exit code 127")
        sys.exit(127)
    except requests.exceptions.ConnectionError:
        print()
        print(f" [Fatal] Could not reach vidsrc.to")
        print(f" [Fatal] This might be because of an issue with the")
        print(f"         external server, or it might be due to")
        print(f"         that the server is blocked in your region. ")
        print(f" [Fatal] Vidsrc-search terminating with exit code -1")
        sys.exit(127)
    except requests.exceptions.RequestException as e:
        print()
        print(f" [Fatal] An unknown network error occured: {e}")
        print(f" [Fatal] This could be due to an issue with the server")
        print(f" [Fatal] Vidsrc-search terminating with exit code 255")
        sys.exit(255)
    return


def cleanup() -> None:
    print(" [Info] Performing program cleanup process")
    path_one = os.path.expanduser("~/.config/pymovie/movie_buffer")
    path_two = os.path.expanduser("~/.config/pymovie/tv_buffer")
    delete_directory_recursive(path_one)
    delete_directory_recursive(path_two)
    return


def bootstrap() -> None:
    required_path_one = os.path.expanduser("~/.config/pymovie")
    required_path_two = os.path.expanduser("~/.config/pymovie/movie_buffer")
    required_path_three = os.path.expanduser("~/.config/pymovie/tv_buffer")
    
    make_directory(required_path_one)
    make_directory(required_path_two)
    make_directory(required_path_three)

    return
