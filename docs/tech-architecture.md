
Also see the [technical research](https://github.com/SunyataZero/mindfulness-at-the-computer/wiki/Technical-Research) page on the wiki

# Tech architecture

Software | Version | Docs | Support
--- | --- | --- | ---
PyInstaller | - | [link](http://pyinstaller.readthedocs.io/en/stable/) | -
[Python](#python) | 3.x | [link](https://docs.python.org/3/) | [SO](https://stackoverflow.com/questions/tagged/python)
[Qt through PyQt](qt-and-pyqt) | 5.9 | [Qt](http://doc.qt.io/qt-5/) | #pyqt @ freenode IRC, [list](http://wiki.qt.io/Online_Communities)
SQLite through sqlite3 | - | [py module](https://docs.python.org/3/library/sqlite3.html), [official](https://www.sqlite.org/docs.html) | -
[unittest + qttest](unittest-and-qttest) | [unittest](https://docs.python.org/3/library/unittest.html) [qttest](http://doc.qt.io/qt-5/qtest.html)| -


## Dependencies


### Python

At the time of writing we are using Python 3.6

### Qt and PyQt

The Qt and PyQt versions almost always seem to be the same.

Can be installed in different ways (pip on all systems, apt-get on Debian based systems, (install .exe file on Windows?))

## Python modules
(Part of the standard library)

### sqlite3

## Application structure

### update_gui() function

### model and database

## Code Conventions

Here are some things that are different from PEP8 or standard Python recommendations:
* one class per file (plus minor supporting classes)
* 120 chars max per line

### Variable naming

Prefixes: None used at the moment

Suffixes:
* `_l[x]` where `[x]` is a number which describes the level of the widget or layout --- this helps us understand the structure of the application in places where there are nested layouts
  * can also sometimes be `_w[x]` for "layout widgets"
* `_[type]`, for example `_int`


### Continuous Integration

Travis

https://blog.ionelmc.ro/2014/05/25/python-packaging/

https://github.com/codecov/example-python


### Code coverage

For coverage.py to discover the subdirectories of the root dir specified with --source
we need to have an __init__.py file for each directory/package

https://github.com/audreyr/how-to/blob/master/python/use_coverage_with_unittest.rst


## unittest and qttest

http://johnnado.com/pyqt-qtest-example/
https://bitbucket.org/jmcgeheeiv/pyqttestexample/src/
Testing: https://stackoverflow.com/questions/1616228/pyqt-gui-testing/46208135#46208135

#### Travis CI

https://github.com/mikkeloscar/arch-travis/issues/14

pyqt travis
gui testing travis

https://docs.travis-ci.com/user/languages/python/


##### "qxcbconnection: could not connect to display"

We need to enable xvfb to do GUI testing:
https://docs.travis-ci.com/user/gui-and-headless-browsers/#Using-xvfb-to-Run-Tests-That-Require-a-GUI


***

