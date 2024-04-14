import platform

from typing import List
from ..argparsing import ArgumentsError

__version__ = "v0.2.3"


def print_version() -> None:
    """Prints system information and the version of the program"""
    print(f"vidsrc-search {__version__}")
    print(f"{platform.python_implementation().lower()} {platform.python_version().lower()}")
    print(f"{platform.platform(True, True).lower()} {platform.machine().lower()}")
    return


def run_module(arguments: List[str]):
    """Runs the version module"""
    if arguments == ["version"]:
        print_version()
        return
    raise ArgumentsError(f"invalid arguments for command 'help' received: {' '.join(arguments)}")

