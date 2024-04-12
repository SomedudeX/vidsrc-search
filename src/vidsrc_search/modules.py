import sys

from . import utils
from . import library
from . import search

from .argparsing import ArgumentsError

AvailableBaseArguments = ["", "version", "help", "library", "search"]


def start(args: dict) -> None:
    if args["module"] == [""]:
        utils.show_help()
        sys.exit(0)
    if args["module"] == ["version"]:
        utils.show_version()
        sys.exit(0)
    if args["module"] == ["help"]:
        utils.show_help()
        sys.exit(0)
    if args["module"] == ["help", "help"]:
        utils.show_help_help()
        sys.exit(0)
    if args["module"] == ["help", "library"]:
        utils.show_help_lib()
        sys.exit(0)
    if args["module"] == ["help", "search"]:
        utils.show_help_search()
        sys.exit(0)
    if args["module"] == ["library", "download"]:
        library.handle_download()
        sys.exit(0)
    if args["module"] == ["library", "remove"]:
        library.handle_remove()
        sys.exit(0)
    if args["module"] == ["library", "size"]:
        library.get_size()
        sys.exit(0)
    if args["module"][0] == "search":
        if len(args["module"]) == 2:
            search.handle_search(args["module"][1], args["raw"], args["new"])
            sys.exit(0)
    if args["module"][0] not in AvailableBaseArguments:
        raise ArgumentsError(f"'{args['module'][0]}' is not a valid positional command")
    if args["module"][0] == "version":
        raise ArgumentsError(f"expected 0 positional argument for command 'version', got {len(args['module']) - 1} instead")
    if len(args["module"]) == 1:
        raise ArgumentsError(f"command '{args['module'][0]}' requires another positional argument")
    raise ArgumentsError(f"received invalid positional commands: {' '.join(args['module'])}")

