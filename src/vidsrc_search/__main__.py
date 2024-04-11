#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

from . import utils
from . import argparsing


def main():
    try:
        utils.bootstrap()
        argparsing.parse_args()
        print(f" [Info] Finished executing vidsrc-search")
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
    sys.exit(0)


if __name__ == "__main__":
    main()
