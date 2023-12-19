## Pymovie

PyMovie is a terminal utility program that searches [VidSrc](vidsrc.to)'s API to provide movies for free. This exists purely as a proof of concept idea as opposed to a production ready application. Additionally, there exists a virtually unfixable multiprocessing bug on Windows that causes the compiled executable to download files unusually slowly. 

## Installation

**Automatic**

Download the latest version of PyMovie tailored to your operating system from the releases tab, then double click on the application executable. The setup process should automatically begin configuring your system and downloading movie libraries. 

> [!NOTE]
> The movie library that the program downloads is simply a json file. Although it might take a while, rest assured that the program is not filling your disk with massive files without your consent. Additionally, the program will report the amount of space that it had used at the end of the download. 

**Manual (Linux/macOS only)**

- Install Python 3
- Clone the repository

```bash
git clone https://github.com/SomedudeX/PyMovie
cd PyMovie
```

- Install required packages

```bash
pip3 install -r requirements.txt
```

You could stop here and use the python script as it is by running `python3 App/entrypoint.py`, but if wish to build the project into an executable, follow the steps below:

- Install PyInstaller
```bash
pip3 install pyinstaller
```

- Build the project by running

```bash
./setup.sh
``` 

The output file will then be created in the dist folder. 

## Uninstallation
Use the reset option from within the application (Windows/macOS/Linux) or run `uninstall.sh` (macOS/Linux) to delete all configuration files pertinent to the application. 

--

Last updated Jan 2024

Not in active development
