

# PyInstaller

[PyInstaller](http://www.pyinstaller.org/) can be used to build executable files

You have to be using the platform that you are building the executables for


## Building on Ubuntu

* Install version 3.5 of Python (PyInstaller doesn't work with 3.6 at the time of writing)
  * Which version is used will depend on the Ubuntu version, but any version 3.0 - 3.5 should be fine (?)
* `pip install pyinstaller`
* go to the base application directory
* Type `pyinstaller mindfulness-at-the-computer.py`

This process will create an executable file with supporting .so files, however we may want to also create an installation package


We also need to include this:

import glob
my_datas = []
my_datas += glob.glob("user_files")

a.datas = my_datas



## Building on Windows

* Install version 3.5 of Python (PyInstaller doesn't work with 3.6 at the time of writing) with these settings:
  * Install Python only for the current user (otherwise there may be problems with permissions later on)
  * Add the path (you have to restart to get the path working)
* To install PyInstaller: `pip install pyinstaller`
* To install PyQt5: `pip install pyqt5`
* Find the installation path for PyQt5 (example: "C:\Python\Python35\Lib\site-packages\PyQt5\Qt\bin")
* Go to the base application directory
* Type `pyinstaller --paths [pyqt5 install directory] mindfulness-at-the-computer.py`. For example: `pyinstaller --paths C:\Python\P
ython35\Lib\site-packages\PyQt5\Qt\bin mindfulness-at-the-computer.py`
  * "--paths" has to be used: https://stackoverflow.com/questions/42880859/importerror-dll-load-failed-the-specified-module-could-not-be-found-failed-to


### Issues when building for Windows

PyInstaller does not accept the same backslashes (file paths) as when running from source


## Building on Mac

TBD


# py2exe

http://www.py2exe.org/


# cx_freeze

https://anthony-tuininga.github.io/cx_Freeze/


## AppImage

Maybe not the best solution:

> Due to the way Python imports work and due to the way Python packages are installed on Debian and Ubuntu, it is not trivial to create working AppDirs from them.

https://github.com/probonopd/AppImages/tree/master/recipes

https://github.com/AppImage/AppImageKit/wiki/Creating-AppImages


