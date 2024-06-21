import os
import sys
import inspect


class CallerInfo:
    """The info of the caller of the function"""
    lineno = -1
    filename = ""


class Logger:
    """A Logger class that prints to the console"""

    def __init__(
        self,
        emit: bool = False
    ) -> None:
        """Initiates a Logger class"""
        self.emit = emit
        return

    def change_emit_level(
        self,
        new_emit: bool = False
    ) -> None:
        """Sets a new emit level; anything above this level will be logged"""
        self.emit = new_emit
        return

    def log(
        self,
        message: str,
    ) -> None:
        """Log the specified message to the console with `info` severity"""
        if not self.emit:
            return
        caller = get_caller_info()
        if supports_color():
            print("\033[2m", end="")
        else:
            print(" ==> ", end="")
        header = f"{caller.filename}:{caller.lineno}"
        print(f"{header} {message}")
        if supports_color():
            print("\033[0m", end="")
        return


def check_tty():
    """Checks whether the console is a tty, and print a warning if not"""
    if not (hasattr(sys.stdout, "isatty") or sys.stdout.isatty()):
        print(" • warning: vidsrc-search is not being run in a tty")
        print(" • warning: some features may not work correctly")


def get_caller_info() -> CallerInfo:
    """Gets the information of the caller of the function via python inspect"""
    stacktrace = inspect.stack()
    frame_info = inspect.getframeinfo(stacktrace[2][0])
    if sys.platform == "win32":
        filename = frame_info.filename.split("\\")
    else:
        filename = frame_info.filename.split("/")
    ret = CallerInfo()
    ret.filename = filename[len(filename) - 1]
    ret.lineno = frame_info.lineno
    return ret


def ansi_code_patch() -> None:
    """Wrap standard output in an ANSI filter if the terminal does not support
    ansi codes. This is to prevent the program and its dependeicies (namely
    tqdm) from printing garbage text onto the console
    """
    if supports_color():
        return

    import sys
    import re
    import io

    class AnsiFilter(io.TextIOBase):
        def __init__(self, stream):
            self.stream = stream
            self.buffer = stream.buffer

        def write(self, data):
            ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
            self.stream.write(ansi_escape.sub('', data))
            self.stream.flush()

    # Create instances of AnsiFilter for sys.stdout and sys.stderr
    sys.stdout = AnsiFilter(sys.stdout)
    sys.stderr = AnsiFilter(sys.stderr)


def supports_unicode():
    """Returns Trueif the terminal supports unicode, false otherwise"""
    if sys.stdout.encoding != None:
        return sys.stdout.encoding.lower().startswith('utf')
    return False


def supports_color():
    """
    Return True if the running system's terminal supports color,
    and False otherwise. Taken from https://github.com/django/django/blob/
    47c608202a58c8120d049c98d5d27c4609551d33/django/core/management/color.py#L28
    """

    def vt_codes_enabled_in_windows_registry():
        """
        Check the Windows Registry to see if VT code handling has been enabled
        by default, see https://superuser.com/a/1300251/447564.
        """
        try:
            # winreg is only available on Windows.
            import winreg
        except ImportError:
            return False
        else:
            try:
                reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Console") # type: ignore
                reg_key_value, _ = winreg.QueryValueEx(reg_key, "VirtualTerminalLevel") # type: ignore
            except FileNotFoundError:
                return False
            else:
                return reg_key_value == 1

    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

    return is_a_tty and (
        sys.platform != "win32"
        or "ANSICON" in os.environ
        or
        # Windows Terminal supports VT codes.
        "WT_SESSION" in os.environ
        or
        # Microsoft Visual Studio Code's built-in terminal supports colors.
        os.environ.get("TERM_PROGRAM") == "vscode"
        or vt_codes_enabled_in_windows_registry()
    )


def enable_debug() -> None:
    """Enables debug mode for all modules"""
    from .modules import LogModules
    from .utils import LogUtils

    LogModules.change_emit_level(new_emit=True)
    LogUtils.change_emit_level(new_emit=True)

    from .core.help import LogHelp
    from .core.library import LogLibrary
    from .core.search import LogSearch
    from .core.version import LogVersion

    LogHelp.change_emit_level(new_emit=True)
    LogLibrary.change_emit_level(new_emit=True)
    LogSearch.change_emit_level(new_emit=True)
    LogVersion.change_emit_level(new_emit=True)
