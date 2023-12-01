## Pymovie

PyMovie is a terminal utility program that searches [VidSrc](vidsrc.to)'s API to provide movies for free. 

### Installation

**Automatic**

The installation and setup is relatively simple; download the latest version of PyMovie tailored to your operating system, then double click on the application executable. The setup process should automatically begin configuring your system and downloading movie libraries. 

> [!NOTE]
> The movie library that the program downloads is simply a json file. Although it might take a while, which is due to having to constantly switch downloads (VidSrc stores their library in more than 2000 json files), rest assured that the program is not filling your disk with massive files without your consent. Additionally, the program will report the amount of space that it had used at the end of the download. 

**Manual (Linux/macOS only)**

If you are running Linux (or for whatever reason you want extra hassle), and you need to install the program manually, you need to download a couple of packages first. All of these packages can all be downloaded through `pip3`:

* Cinemagoer
* Requests
* TheFuzz
* PyInstaller

Next, clone the repository by running the following commands: 

```bash
git clone https://github.com/SomedudeX/PyMovie
cd PyMovie
```

You could stop here and use the python script as it is by running `App/entrypoint.py`, but if you would like to build the project into an executable, then you will need to install PyInstaller. Then, you can build the project by either running `./setup.sh` or manually typing `pyinstaller App/entrypoint.py -onefile --name PyMovie`. 

The output file will then be created in the dist folder. 

### Development

This app is more of a side-project, hence development would mostly be bug fixes. That said, you are welcomed to make a pull request and contribute to it. 
