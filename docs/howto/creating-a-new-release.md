


## 1. Building binaries

Semantic versioning is used: semver.org

PyInstaller is used for building

Documentation:
* Command line: http://pyinstaller.readthedocs.io/en/stable/usage.html
* Spec files: http://pyinstaller.readthedocs.io/en/stable/spec-files.html


### Building on Ubuntu

1. Install version 3.5 of Python (PyInstaller doesn't work with 3.6 at the time of writing)
  * Which version is used will depend on the Ubuntu version, but any version 3.0 - 3.5 should be fine (?)
2. `pip install pyinstaller`
3. Go to the base application directory
4. `pyinstaller mindfulness-at-the-computer.py mindfulness-at-the-computer-linux.spec`

This process will create an executable file with supporting .so files

The .spec file has been customized to include the user_files and icons directories

Creating the tar.gz file: `tar -czvf mindfulness-at-the-computer.tar.gz mindfulness-at-the-computer/`

### Building on Windows

1. Install version 3.5 of Python (PyInstaller doesn't work with 3.6 at the time of writing). Use these settings:
  * Install Python only for the current user (otherwise there may be problems with permissions later on)
  * Add the path (you have to restart to get the path working)
2. `pip install pyinstaller`
3. `pip install pyqt5`
4. Find the installation path for PyQt5 (example: "C:\Python\Python35\Lib\site-packages\PyQt5\Qt\bin")
5. Go to the base application directory
6. `pyinstaller --paths [pyqt5 install directory] mindfulness-at-the-computer-windows.spec`. For example: `pyinstaller --paths C:\Python\P ython35\Lib\site-packages\PyQt5\Qt\bin mindfulness-at-the-computer-windows.spec`
  * `--paths` has to be used: https://stackoverflow.com/questions/42880859/importerror-dll-load-failed-the-specified-module-could-not-be-found-failed-to

The resulting exe and dll files will be in the `./dist` directory.

As a last step you can create a zip file

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

