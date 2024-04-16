#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

from . import utils
from . import modules
from . import argparsing

from .argparsing import ArgumentsError


def main() -> int:
    try:
        args = argparsing.parse_arguments(sys.argv)
        utils.initialize(args)
        return modules.start(args)
    except UserWarning:
        print(f" • vidsrc-search received user warning")
        print(f" • vidsrc-search terminating with exit code 1")
        return 1
    except KeyboardInterrupt:
        print(f"\n • vidsrc-search received keyboard interrupt")
        print(f" • vidsrc-search terminating with exit code 1")
        return 1
    except ArgumentsError as e:
        print(f" • inapt arguments: {e.message}")
        print(f" • vidsrc-search terminating with exit code {e.code}")
        return e.code
    except Exception as e:
        name = re.sub(r"(?<!^)(?=[A-Z])", " ", type(e).__name__).lower()
        print(f"\n • {str(e).lower()}")
        print(f" • vidsrc-search received an unknown {name}")
        print(f" • vidsrc-search terminating with exit code 255")
        return 255
    finally:
        # Cleanup needs to happen no matter what
        utils.cleanup()


if __name__ == "__main__":
    sys.exit(main())
