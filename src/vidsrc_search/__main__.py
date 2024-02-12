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
    except KeyboardInterrupt:
        print()
        print(" [Warning] Vidsrc-search received KeyboardInterrupt")
        print(" [Warning] Program force quitting with os._exit()")
        print(" [Warning] Performing program cleanup process")
        utils.cleanup()
        os._exit(0)
    except Exception as e:
        print()
        print(f" [Fatal] An unknown error was encountered during the execution of Vidsrc-search")
        print(f" [Fatal] Error message from program: {e}")
        print(f" [Fatal] Performing program cleanup process")
        utils.cleanup()
        sys.exit(129)


if __name__ == "__main__":
    main()
