## Overview

Vidsrc-search is a command-line utility program that searches [VidSrc](https://vidsrc.to)'s API to provide movies for free.

## Installation

```bash
pip install --upgrade vidsrc-search
vidsrc-search help
```

## Usage

```
Usage: vidsrc-search <command> [option] [flags]

Available commands:
    help        shows this menu
    search      search a movie by name
    library     actions regarding the movie lib

Use 'vidsrc-search help <command>' for info on a
specific command. Arguments are parsed strictly in
the order above
```

## Implementation

VidSrc provides an API to access links to specific movies hosted on their website. When you select a movie to be viewed, this program will cache the site data from VidSrc into an html file stored on disk. The program then does some proprocessing to the html webpage to remove annoying ad/redirect elements.

If you would like to view the raw website without preprocessing, you can disable this feature using the `--raw` flag. Additionally, you can use the `--new` flag to re-cache an already cached website.

