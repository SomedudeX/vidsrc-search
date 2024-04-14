from typing import Any, Dict, List, Tuple


class ArgumentsError(Exception):
    """An error encountered when parsing arguments"""
    def __init__(
        self,
        message: str,
        code: int = 1
    ) -> None:
        """Initializes an ArgumentsError instance"""
        self.message = message
        self.code = code
        super().__init__()
        return


def is_flag(arg: str) -> bool:
    """Whether an item from sys.argv is a flag"""
    return len(arg) >= 1 and \
           arg[0] == "-"


def is_int(arg: str) -> bool:
    """Whether an item from sys.argv is an integer"""
    return len(arg) >= 1 and \
           arg.isdigit()


def is_stacked_flag(flag: str) -> bool:
    """Whether an argument is a stacked flag (e.g. -abc)"""
    return len(flag) >= 1 and \
           flag[0] == "-" and \
           flag[1] != "-"


def split_arguments(argv: List[str]) -> Tuple[Any, Any]:
    """Splits arguments into positionals and flags. This is responsible
    for enforcing the structure of the arguments (positionals before flags)
    """
    for index, argument in enumerate(argv):
        if is_flag(argument):
            flags = argv[index:]
            positionals = argv[:index]
            return positionals, flags
    return argv, []


def parse_arguments(argv: List[str]) -> Dict[str, Any]:
    """Parse the arguments from sys.argv into a dictionary"""
    positionals, flags = split_arguments(argv[1:])
    parsed_arguments = {
        "module": [""],
        "raw": False,
        "new": False
    }

    if len(positionals) > 0:
        parsed_arguments["module"] = positionals

    for flag in flags:   # Mapping each command line flag to a dictionary key
        if flag == "--raw" or flag == "-r":
            parsed_arguments["raw"] = True
            continue
        if flag == "--new" or flag == "-n":
            parsed_arguments["new"] = True
            continue
        if is_stacked_flag(flag[0]):
            raise ArgumentsError(f"stacked flag '{flag[0]}' not allowed", 1)
        raise ArgumentsError(f"invalid flag '{flag[0]}' received", 1)
    return parsed_arguments
