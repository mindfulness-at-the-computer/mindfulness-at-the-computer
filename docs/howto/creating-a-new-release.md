## 1. Building binaries

Semantic versioning is used: semver.org

PyInstaller is used for building, it bundles almost everything into a distribution package. Please note: After having created a package using PyInstaller the user doesn't need to worry about dependencies, with the exception of [libc on Linux-based systems](https://pyinstaller.readthedocs.io/en/stable/usage.html#making-linux-apps-forward-compatible)

Documentation:
* Command line: http://pyinstaller.readthedocs.io/en/stable/usage.html
* Spec files: http://pyinstaller.readthedocs.io/en/stable/spec-files.html


### Building on Ubuntu

1. Install Python (PyInstaller now works with version 3.6 of Python): `sudo apt-get install python3`
1. `sudo apt-get install python3-pip`
1. `sudo pip3 install pyinstaller`
   * Please verify that you can access pyinstaller by trying to run `pyinstaller` from the command line
1. `sudo pip3 install pyqt5`
1. Go to the base application directory
1. `pyinstaller mindfulness-at-the-computer-linux.spec`

This process will create an executable file with supporting .so files

The .spec file has been customized to include the user_files and icons directories

Creating the tar.gz file:
1. Go to the `dist` directory
2. `tar -czvf mindfulness-at-the-computer.tar.gz mindfulness-at-the-computer/`

#### glibc

*Please choose a fairly early version of Ubuntu*, 16.04 or earlier. The reason is that pyinstaller does not bundle *libc* into the resulting package so the resulting package may not (will not?) work with earlier versions of libc and Linux:
https://pyinstaller.readthedocs.io/en/stable/usage.html#making-linux-apps-forward-compatible

glibc is also specific for 32 or 64 bit so builds will only work on that architecture. Because of how common 64 bit systems are nowadays this is the priority


### Building on MacOS

1. Install Python (PyInstaller now works with version 3.6 of Python): `brew install python3`
2. Go to the base application directory
3. Create and activate a virtual environment: see [this article](using-virtual-environment.md)
4. Install pyinstaller: `pip install pyinstaller`
5. `pyinstaller --windowed mindfulness-at-the-computer-macos.spec`. This will give you a `dist` folder with two subfolders:
    - mindfulness-at-the-computer
    - mindfulness-at-the-computer.app
6. Keep `mindfulness-at-the-computer.app` and delete the other folder
7. Go to the `dist` folder and add a symlink to the /Applications folder: `ln -s /Applications Applications`. 
   PyCharm might not like this and start indexing the Applications folder as well.
   You might want to close PyCharm before doing this.
8. Open the disk utilities with spotlight `cmd-space utility`
9. Create a new dmg file: `cmd-shift-n`
10. Select the dist folder in your project. 
11. In the `Save As` field enter the name of the dmg file: `mindfulness-at-the-computer`
12. From the `Image Format` drop-down select `read only` then click `Save`

You will now have a mindfulness-at-the-computer.dmg file at the selected location.


### Building on Windows

1. Install Windows
   * It seems to be better to build on Windows 7. The Windows 10 build binary file has failed to start for us, but the Windows 7 has always worked once the build has been completed. More info here: http://pyinstaller.readthedocs.io/en/stable/usage.html#windows
   * If you build on Windows 7 please make sure that SP1 (service pack 1) is installed, as this is needed for the Python installer to run
2. Install Python (PyInstaller works with 3.6 which is the latest Python version at the time of writing). *Please use these settings*:
   * Install Python *only for the current user* (otherwise there may be problems with permissions later on)
   * *Add the path* (you have to restart to get the path to work)
3. Start cmd *with admin privelige*
   * We need admin priveliges, otherwise we may get permission denied for the PyQt files
4. `pip install pyqt5`
   * or if it been installed previously: `pip install pyqt5 --upgrade`
5. `pip install pyinstaller`
   * or if it been installed previously: `pip install pyinstaller --upgrade`
   * Please note that the pyinstaller version may not be compatible with the latest python version. (At the time of writing this is not a problem, but it has been in the past)
6. Find and copy the installation path for PyQt5 (example: `C:\Python\Python35\Lib\site-packages\PyQt5\Qt\bin`)
7. Create an empty directory where you can unzip the files, preferrably with a path without any spaces
8. Download the latest code (can be found on the github main page under the green "clone or download" button
9. If you have tried to build previously: Remove the `build` and `dist` directories:
   * `rmdir /s build`
   * `rmdir /s dist`
10. Go to the base application directory
11. `pyinstaller --paths [pyqt5 install directory] mindfulness-at-the-computer-windows.spec`
    * For example: `pyinstaller --paths C:\Python\Python36\Lib\site-packages\PyQt5\Qt\bin mindfulness-at-the-computer-windows.spec`
    * `--paths` has to be used: https://stackoverflow.com/questions/42880859/importerror-dll-load-failed-the-specified-module-could-not-be-found-failed-to
12. Copy all the files in the `dist/mindfulness-at-the-computer/PyQt5/Qt/plugins/platforms` directory to the `dist/mindfulness-at-the-computer/` directory --- the reason is a bug in PyInstaller. This only needs to be done on Windows, and when not doing this we have only had problems on some (a majority) of Windows 10 systems

The resulting `exe` and `dll` files will be in the `./dist/mindfulness-at-the-computer` directory. (There will also be an executable in the `./build/mindfulness-at-the-computer` directory but this should not be used because it has the wrong references)

As the last step, you can create a zip file from all the contents of the `./dist/mindfulness-at-the-computer` directory

Please verify that there is an `.exe` file (`mindfulness-at-the-computer.exe`) and try to run it. Important that this is done after creating the zip file because otherwise the user will start the application with a db file already existing and with an incorrect audio path as well as not showing the intro wizard



## 2. Manual testing

The most important things to test after building:
1. Start by unzipping the file (rather than starting with the result of the build, since this will risk that the application is distributed with a db file inside the zip file)
2. Verify that the intro wizard is shown
3. Verify that the audio is playing
4. Verify that the breathing notifications, breathing dialogs and rest reminder and rest fullscreen window can be seen
5. Verify that you can the application behaves as expected with regards to closing, opening, minimizing to task bar, minimizing to system tray
6. Verify that you can add a new entry in the breathing phrase list
7. Verify that you can add a new entry in the rest action list



## 3. Publishing

### Creating a new GitHub release

https://github.com/mindfulness-at-the-computer/mindfulness-at-the-computer/releases

### Uploading

Upload the archive files (tar.gz, zip, {mac?}) created in the "Building binaries" sections above


## 4. Notifying people of the new version

### Newsletter

https://app.tinyletter.com

### Other outreach

There's a list of places that may be interested in the application on the wiki:
https://github.com/mindfulness-at-the-computer/mindfulness-at-the-computer/wiki/Outreach

Some of these places we have already made a page or post, and in these cases maybe we don't need to do anything (unless we are moving from alpha to beta.)
