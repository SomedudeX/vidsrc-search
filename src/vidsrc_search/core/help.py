from typing import Any, Dict, List

from ..argparsing import ArgumentsError
from ..utils import Logger

LogHelp = Logger()


HELP = """\
usage: vidsrc-search <command> [option] [flags]

available commands:
    help        shows this menu
    version     displays version info
    search      search a movie by its name
    library     actions regarding the movie lib

optional flags:
    -d, --debug enables debug logging and disables
                certain features (e.g. progressbar)

use 'vidsrc-search help <command>' for info on a
specific command. arguments are strictly parsed in
the order specified above. when filing a bug report,
please be sure to use the '--debug' flag in log.\
"""


HELP_HELP = """\
usage: vidsrc-search help [option]

available options:
    help        shows detailed help for 'help'
    version     shows detailed help for 'version'
    search      shows detailed help for 'search'
    library     shows detailed help for 'library'

example usage:
    vidsrc-search help library
    vidsrc-search help help\
"""


HELP_VERSION = """\
usage: vidsrc-search version

displays the program version and relevant system
info. please include the output of this command
when filing a bug report.

example usage:
    vidsrc-search version\
"""


HELP_SEARCH = """\
usage: vidsrc-search search <option> [flags]

required option:
    <str>       a movie title that you would like
                vidsrc-search to search for

optional flags:
    -r, --raw   when this flag is specified, the
                program will open the original
                website instead of caching the html
    -n, --new   when this flag is specified, the
                program will re-cache the html to
                your computer from vidsrc.to

example usage:
    vidsrc-search search 'oppenheimer'
    vidsrc-search search 'avatar'

the optional flags will have no effect with commands
other than 'search'\
"""


HELP_LIB = """\
usage: vidsrc-search library <option>

required options:
    size        prints the program's disk usage
    remove      removes the movies library
    download    downloads the latest movies library
                from https://vidsrc.to

example usage:
    vidsrc-search library download\
"""


def run_module(modules: List[str], args: Dict[str, Any]) -> None:
    """Runs the help module and prints help"""
    if args["dbg"]:
        LogHelp.change_emit_level(True)
        LogHelp.log(f"arguments received by help: {modules}")
    if modules == ["help", "library"]:
        print(HELP_LIB)
        return
    if modules == ["help", "search"]:
        print(HELP_SEARCH)
        return
    if modules == ["help", "version"]:
        print(HELP_VERSION)
        return
    if modules == ["help", "help"]:
        print(HELP_HELP)
        return
    if modules == [""] or modules == ["help"]:
        print(HELP)
        return
    raise ArgumentsError(f"invalid arguments for command 'help' received: {' '.join(modules)}")
