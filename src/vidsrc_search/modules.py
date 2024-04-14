from typing import Any, Dict

from .core import help
from .core import version
from .core import library
from .core import search

from .argparsing import ArgumentsError


def start(args: Dict[str, Any]) -> int:
    """Runs the module parsed by argparsing.parse_arguments"""
    modules = args["module"]
    if modules[0] == "search":
        search.run_module(modules, args)
        return 0
    if modules[0] == "library":
        library.run_module(modules)
        return 0
    if modules[0] == "version":
        version.run_module(modules)
        return 0
    if modules[0] == "help" or modules[0] == "":
        help.run_module(modules)
        return 0
    raise ArgumentsError(f"received invalid positional commands: {' '.join(args['module'])}")
