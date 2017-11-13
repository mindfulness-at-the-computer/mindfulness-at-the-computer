


## 1. Building binaries

Semantic versioning is used: semver.org

PyInstaller is used for building, it bundles almost everything into a distribution package. Please note: After having created a package using PyInstaller the user doesn't need to worry about dependencies, with the exception of [libc on Linux-based systems](https://pyinstaller.readthedocs.io/en/stable/usage.html#making-linux-apps-forward-compatible)

Documentation:
* Command line: http://pyinstaller.readthedocs.io/en/stable/usage.html
* Spec files: http://pyinstaller.readthedocs.io/en/stable/spec-files.html


### Building on Ubuntu

*Please choose a fairly early version*, 16.04 or earlier. The reason is that pyinstaller does not bundle *libc* into the resulting package so the resulting package may not (will not?) work with earlier versions of libc and Linux:
https://pyinstaller.readthedocs.io/en/stable/usage.html#making-linux-apps-forward-compatible

1. Install Python (PyInstaller now works with version 3.6 of Python): `sudo apt-get install python3`
2. `pip3 install pyinstaller`
3. `pip3 install pyqt5`
3. Go to the base application directory
4. `pyinstaller mindfulness-at-the-computer-linux.spec`

This process will create an executable file with supporting .so files

The .spec file has been customized to include the user_files and icons directories

Creating the tar.gz file: `tar -czvf mindfulness-at-the-computer.tar.gz mindfulness-at-the-computer/`

### Building on MacOS


### Building on Windows

1. Install Python (PyInstaller works with 3.6 which is the latest Python version at the time of writing). Use these settings:
  * Install Python only for the current user (otherwise there may be problems with permissions later on)
  * Add the path (you have to restart to get the path working)
2. `pip install pyinstaller`
3. `pip install pyqt5`
4. Find the installation path for PyQt5 (example: "C:\Python\Python35\Lib\site-packages\PyQt5\Qt\bin")
5. Go to the base application directory
6. `pyinstaller --paths [pyqt5 install directory] mindfulness-at-the-computer-windows.spec`. For example: `pyinstaller --paths C:\Python\Python35\Lib\site-packages\PyQt5\Qt\bin mindfulness-at-the-computer-windows.spec`
  * `--paths` has to be used: https://stackoverflow.com/questions/42880859/importerror-dll-load-failed-the-specified-module-could-not-be-found-failed-to

The resulting exe and dll files will be in the `./dist` directory.

As a last step you can create a zip file

#### Windows 7 and 10

It seems to be better to build on Windows 7. The Windows 10 build binary file has failed to start for us, but the Windows 7 has always worked once the build has been completed

### Building on Mac

TBD


## 2. Manual testing



## 3. Publishing

### Creating a new github release

https://github.com/SunyataZero/mindfulness-at-the-computer/releases

### Uploading

Upload the archive files (tar.gz, zip, {mac?}) created in the "Building binaries" sections above


## 4. Notifying people of the new version

### Newsletter

https://app.tinyletter.com

### Other outreach

There's a list of places that may be interested in the application on the wiki:
https://github.com/SunyataZero/mindfulness-at-the-computer/wiki/Outreach

Some of these places we have already made a page or post, and in these cases maybe we don't need to do anything (unless

If moving from alpha to beta

