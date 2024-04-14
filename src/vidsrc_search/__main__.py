#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from . import utils
from . import modules
from . import argparsing

from .argparsing import ArgumentsError


def main() -> int:
    try:
        utils.initialize()
        args = argparsing.parse_arguments(sys.argv)
        return modules.start(args)
    except UserWarning:
        utils.newline_cursor()
        print(f"warning: vidsrc-search received user warning")
        print(f"warning: vidsrc-search terminating with exit code 1")
        return 1
    except KeyboardInterrupt:
        utils.newline_cursor()
        print(f"warning: vidsrc-search received keyboard interrupt")
        print(f"warning: vidsrc-search terminating with exit code 1")
        return 1
    except ArgumentsError as e:
        utils.newline_cursor()
        print(f"fatal: {e.message}")
        print(f"fatal: vidsrc-search received an arguments error")
        print(f"fatal: vidsrc-search terminating with exit code {e.code}")
        return e.code
    except Exception as e:
        utils.newline_cursor()
        print(f"fatal: {str(e).lower()}")
        print(f"fatal: vidsrc-search received and unknown {type(e).__name__.lower()}")
        print(f"fatal: vidsrc-search terminating with exit code 255")
        return 255
    finally:
        utils.cleanup()


if __name__ == "__main__":
    sys.exit(main())
