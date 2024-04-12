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
        print(" [Warning] Vidsrc-search received UserWarning")
        print(" [Warning] Program force quitting with os._exit(0)")
        utils.cleanup()
        os._exit(0)
    except KeyboardInterrupt:
        print()
        print(" [Warning] Vidsrc-search received KeyboardInterrupt")
        print(" [Warning] Program force quitting with os._exit(0)")
        utils.cleanup()
        os._exit(0)
    except ArgumentsError as e:
        print(f" [Fatal] Vidsrc-search has encountered an error during arguments parsing")
        print(f" [Fatal] ArgumentsError: {e.message}")
        print(f" [Fatal] Vidsrc-search terminating with exit code {e.code}")
        sys.exit(e.code)
    except BaseException as e:
        print()
        print(f" [Fatal] An unknown error was encountered during the execution of vidsrc-search")
        print(f" [Fatal] {type(e).__name__}: {e}")
        utils.cleanup()
        print()
        print(f" [Info] Note: ")
        print(f" [Info] This might be due to a temporary error with the program or an external server")
        print(f" [Info] The issue might fix itself if wait a bit and rerun the program")
        print(f" [Info] Vidsrc-search terminating with exit code 255")
        sys.exit(255)


if __name__ == "__main__":
    main()
