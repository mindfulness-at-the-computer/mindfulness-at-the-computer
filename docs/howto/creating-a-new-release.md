


## 1. Building binaries

Determining the version number. Semantic versioning is used: semver.org

### Linux
There's a .spec file for linux

### Windows
There's a .spec file for windows
PLEASE NOTE: The path for the Qt binaries have been hard-coded






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
6. TBD: CHECK IF WE CAN GIVE ONE PATH AT COMMAND LINE AND ANOTHER INSIDE THE SPEC FILE `pyinstaller --paths [pyqt5 install directory] mindfulness-at-the-computer-windows.spec`. For example: `pyinstaller --paths C:\Python\P ython35\Lib\site-packages\PyQt5\Qt\bin mindfulness-at-the-computer-windows.spec`
  * `--paths` has to be used: https://stackoverflow.com/questions/42880859/importerror-dll-load-failed-the-specified-module-could-not-be-found-failed-to

### Building on Mac

TBD




## 2. Manual testing



## 3. Publishing

### Creating a new github release


## 4. Notifying people of the new version

### Newsletter

https://app.tinyletter.com

### Social media



