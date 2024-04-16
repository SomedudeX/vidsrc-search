from typing import Any, Dict

from .core import help
from .core import version
from .core import library
from .core import search

from .argparsing import ArgumentsError
from .utils import Logger

LogModules = Logger()


def start(args: Dict[str, Any]) -> int:
    """Runs the module parsed by argparsing.parse_arguments"""
    modules = args["module"]
    if modules[0] == "search":
        LogModules.log("starting module search")
        search.run_module(modules, args)
        return 0
    if modules[0] == "library":
        LogModules.log("starting module library")
        library.run_module(modules, args)
        return 0
    if modules[0] == "version":
        LogModules.log("starting module version")
        version.run_module(modules, args)
        return 0
    if modules[0] == "help" or modules[0] == "":
        LogModules.log("starting module help")
        help.run_module(modules, args)
        return 0
    raise ArgumentsError(f"received invalid positional commands: {' '.join(args['module'])}")
