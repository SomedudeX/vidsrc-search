#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import warnings

warnings.filterwarnings("ignore")

from . import utils
from . import argparsing


def main():
    try:
        utils.bootstrap()
        argparsing.parse_args()
        utils.cleanup()
    except KeyboardInterrupt:
        print()
        print(" [Warning] Vidsrc-search received KeyboardInterrupt")
        print(" [Warning] Program force quitting with os._exit()")
        utils.cleanup()
        os._exit(0)
    except UserWarning:
        print(" [Warning] Vidsrc-search received UserWarning")
        print(" [Warning] Program force quitting with os._exit()")
        utils.cleanup()
        os._exit(0)
    except Exception as e:
        print()
        print(f" [Fatal] An unknown error was encountered during the execution of vidsrc-search")
        print(f" [Fatal] Error message from program: {e}")
        utils.cleanup()
        print()
        print(f" [Info] Note: ")
        print(f" [Info] This might be due to a temporary error in the program")
        print(f" [Info] The issue might fix itself if you rerun the program")
        print(f" [Info] Vidsrc-search terminating with exit code 255")
        sys.exit(255)


if __name__ == "__main__":
    main()
