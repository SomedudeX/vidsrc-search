from typing import List, Tuple, Dict, Any, Union


class ArgumentsError(Exception):
    def __init__(
        self,
        message: str,
        code: int = 1
    ) -> None:
        self.message = message
        self.code = code
        super().__init__()


def is_flag(arg: str) -> bool:
    assert len(arg) > 0
    return arg[0] == "-"


def is_int(arg: str) -> bool:
    if not isinstance(arg, str):
        return False
    return arg.isdigit()


def is_stacked_flag(flag: str) -> bool:
    if len(flag) <= 2:
        return False
    return flag[0] == "-" and flag[1] != "-"


def process_bool_flag(flag: tuple) -> Union[int, str]:
    if not is_int(flag[1]):
        return flag[1]
    return bool(int(flag[1]))


def split_arguments(argv: List[str]) -> Tuple[Any, Any]:
    for index, arg in enumerate(argv):
        if is_flag(arg):
            flags = argv[index:]
            positionals = argv[:index]
            return positionals, split_flags(flags)
    return argv, []


def split_flags(flags: List[str]) -> List[Tuple]:
    ret = []
    for _ in range(len(flags)):
        if len(flags) == 0:
            break
        current_flag = flags[0]
        if current_flag[0] == "-":
            option = current_flag
            ret.append((option, True))
            del flags[0]
            continue
        raise ArgumentsError(f"error parsing '{current_flag}' (unexpected trailing positional)", 1)
    return ret


def parse_arguments(argv: List[str]) -> Dict[str, Any]:
    ret = {
        "module": [""],
        "raw": False,
        "new": False
    }

    positionals, flags = split_arguments(argv)

    if len(positionals) > 0:
        ret["module"] = positionals

    for flag in flags:   # Mapping each command line flag to a dictionary key
        if flag[0] == "--raw" or flag[0] == "-r":
            ret["raw"] = process_bool_flag(flags[0])
            continue
        if flag[0] == "--new" or flag[0] == "-n":
            ret["new"] = process_bool_flag(flags[0])
            continue
        if is_stacked_flag(flag[0]):
            raise ArgumentsError(f"stacked flag '{flag[0]}' not allowed", 1)
        raise ArgumentsError(f"invalid flag '{flag[0]}' received", 1)
    return ret
