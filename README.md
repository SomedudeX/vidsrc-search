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
    search      search a movie by name
    library     actions regarding the movie lib

use 'vidsrc-search help <command>' for info on a
specific command. arguments are strictly parsed in
the order specified above
```

## Implementation

VidSrc provides an API to access links to specific movies hosted on their website. When you select a movie to be viewed, this program will cache the site data from VidSrc into an html file stored on disk. The program then does some preprocessing to the html webpage to remove annoying ad/redirect elements.

If you would like to view the raw website without preprocessing, you can disable this feature using the `--raw` flag. Additionally, you can use the `--new` flag to re-cache an already cached website.

## Contributing

Opening issues are the preferred way of contributing. Please include the steps to reproduce, what you expected to happen versus what actually happened, as well as the output of `vidsrc-search version` in your issue.

When filing issues, please also make sure that you are using `vidsrc-search` by directly cloning the repository as opposed to downloading from pip. This will make sure you have the most up-to-date version of `vidsrc-search`.
