#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from . import utils
from . import modules
from . import argparsing

from .argparsing import ArgumentsError


def main():
    try:
        sys.argv = sys.argv[1:]
        utils.bootstrap()
        args = argparsing.parse_arguments(sys.argv)
        modules.start(args)
    except SystemExit as e:
        sys.exit(e.code)
    except UserWarning:
        print("warning: vidsrc-search received UserWarning")
        print("warning: program force quitting with os._exit(0)")
        utils.cleanup()
        os._exit(0)
    except KeyboardInterrupt:
        print()
        print("warning: vidsrc-search received KeyboardInterrupt")
        print("warning: program force quitting with os._exit(0)")
        utils.cleanup()
        os._exit(0)
    except ArgumentsError as e:
        print(f"fatal: vidsrc-search has encountered an error during arguments parsing")
        print(f"fatal: argumentsError: {e.message}")
        print(f"fatal: vidsrc-search terminating with exit code {e.code}")
        sys.exit(e.code)
    except BaseException as e:
        print()
        print(f"fatal: an unknown error was encountered during the execution of vidsrc-search")
        print(f"fatal: {type(e).__name__}: {e}")
        utils.cleanup()
        print()
        print(f"info: note: ")
        print(f"info: this might be due to a temporary error with the program or an external server")
        print(f"info: the issue might fix itself if wait a bit and rerun the program")
        print(f"info: vidsrc-search terminating with exit code 255")
        sys.exit(255)


if __name__ == "__main__":
    main()
