import sys

from . import utils
from . import search
from . import download
from . import uninstall


def parse_command_opt() -> None:
    _argv = sys.argv
    
    if _argv[1] == "help":
        if _argv[2] == "help":
            utils.show_help_help()
            return
        elif _argv[2] == "search":
            utils.show_help_search()
            return
        elif _argv[2] == "library":
            utils.show_help_lib()
            return
        else:
            print(f" [Fatal] Invalid argument for help: '{_argv[2]}'")
            print(f" [Fatal] Use 'vidsrc-search help' for usage info")
            print(f" [Fatal] Vidsrc-search terminating with exit code 1")
            sys.exit(1)
            
    if _argv[1] == "search":
        search.handle_search(_argv[2])
        return
         
    if _argv[1] == "library":
        if _argv[2] == "download":
            download.handle_download()
            return
        elif _argv[2] == "remove":
            uninstall.handle_remove()
            return
        else:
            print(f" [Fatal] Invalid argument for library: {_argv[2]}")
            print(f" [Fatal] Use 'vidsrc-search help library' for usage info")
            print(f" [Fatal] Vidsrc-search terminating with exit code 1")
            sys.exit(1)
    
    print(f" [Fatal] Invalid argument: {_argv[1]}")
    print(f" [Fatal] Vidsrc-search terminating with exit code 1")
    sys.exit(1)


def parse_command() -> None:
    # Initiated when there exists only one command-line arg
    _argv = sys.argv
    
    if _argv[1] == "help":
        utils.show_help()
        return
    elif _argv[1] == "search":
        print(f" [Fatal] Command 'search' requires a query")
        print(f" [Fatal] Use 'vidsrc-search help search' for usage info")
        print(f" [Fatal] Vidsrc-search terminating with exit code 1")
        sys.exit(1)
    elif _argv[1] == "library":
        print(f" [Fatal] Command 'library' requires another argument")
        print(f" [Fatal] Use 'vidsrc-search help library' for usage info")
        print(f" [Fatal] Vidsrc-search terminating with exit code 1")
        sys.exit(1)
    else:
        print(f" [Fatal] Invalid argument: '{_argv[1]}'")
        print(f" [Fatal] Use 'vidsrc-search help' for usage info")
        print(f" [Fatal] Vidsrc-search terminating with exit code 1")
        sys.exit(1)
    

def parse_args() -> None:
    # The hightest level control-flow for argparsing
    _argv = sys.argv
    _argc = len(_argv)
    
    if _argc == 1:
        utils.show_help()
        return
    if _argc == 2:
        parse_command()
        return
    if _argc == 3:
        parse_command_opt()
        return
    if _argc > 3:
        print(f" [Fatal] Too many arguments provided")
        print(f" [Fatal] Use 'vidsrc-search help' for usage info")
        print(f" [Fatal] Vidsrc-search terminating with exit code 1")
        sys.exit(1)
    
    print(f" [Fatal] An unknown error occured")
    print(f" [Info] Locals:")
    print(f"  - sys.argv = {_argv}")
    print(f"  - sys.argc = {_argc}")
    print(f" [Fatal] Vidsrc-search terminating with exit code -1")
    sys.exit(-1)
    
