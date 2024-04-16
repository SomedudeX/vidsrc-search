## Overview

![GitHub Release](https://img.shields.io/github/v/release/SomedudeX/vidsrc-search?style=for-the-badge) ![PyPI - Status](https://img.shields.io/pypi/status/vidsrc-search?style=for-the-badge) ![PyPI - Downloads](https://img.shields.io/pypi/dm/vidsrc-search?style=for-the-badge)

A command-line utility program that searches [VidSrc](https://vidsrc.to)'s API to provide movies for free.

<img width="1235" alt="Screenshot 2024-04-14 at 19 38 54" src="https://github.com/SomedudeX/vidsrc-search/assets/101906945/58983e3b-8f13-4474-92fe-cb5ad7f37b5f">

## Installation

```bash
pip install --upgrade vidsrc-search
vidsrc-search help
```

## Usage

```
usage: vidsrc-search <command> [option] [flags]

available commands:
    help        shows this menu
    version     displays version info
    search      search a movie by its name
    library     actions regarding the movie lib

optional flags:
    -d, --debug enables debug logging and disables
                certain features (e.g. progress bars)

use 'vidsrc-search help <command>' for info on a
specific command. arguments are strictly parsed in the
order specified above. when filing a bug report, please
be sure to use the '--debug' flag in log.
```

## Notes

This project has been tested on the following requirements and platforms:

 * CPython 3.8.19, 3.9.1, 3.12.2
 * Windows 11, macOS 14, Debian Linux

## Contributing

Opening issues on GitHub are the preferred way of contributing. Please include the steps to reproduce, what you expected to happen versus what actually happened, as well as the output of `vidsrc-search` with the `--debug` flag in your issue.

When filing issues, please also make sure that you are using `vidsrc-search` by directly cloning the repository as opposed to downloading from pip. This will make sure you have the most up-to-date version of `vidsrc-search`.

## Links

 * [License](https://github.com/SomedudeX/vidsrc-search/blob/main/LICENSE)
 * [Github](https://github.com/SomedudeX/vidsrc-search)
 * [PyPi](https://pypi.org/project/vidsrc-search/)
