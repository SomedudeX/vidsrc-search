import platform

from typing import Any, Dict, List
from ..argparsing import ArgumentsError
from ..utils import Logger

__version__ = "v0.2.4"
LogVersion = Logger()


def print_version() -> None:
    """Prints system information and the version of the program"""
    print(f" • vidsrc-search {__version__}")
    print(f" • {platform.python_implementation().lower()} {platform.python_version().lower()}")
    print(f" • {platform.platform(True, True).lower()} {platform.machine().lower()}")
    return


def run_module(module: List[str], args: Dict[str, Any]):
    """Runs the version module"""
    if args["dbg"]:
        LogVersion.change_emit_level(new_emit=True)
        LogVersion.log(f"arguments received by version: {module}")
    if module == ["version"]:
        print_version()
        return
    raise ArgumentsError(f"invalid arguments for command 'help' received: {' '.join(module)}")

