
# Tech architecture

## Dependencies

Software | Version | Docs | Support
--- | --- | --- | ---
PyInstaller | - | [link](http://pyinstaller.readthedocs.io/en/stable/) | -
[Python](#python) | 3.5 | [link](https://docs.python.org/3/) | [Gitter](https://gitter.im/mindfulness-at-the-computer/Lobby), [SO](https://stackoverflow.com/questions/tagged/python)
[Qt through PyQt](qt-and-pyqt) | 5.9 | [Qt](http://doc.qt.io/qt-5/) | [Gitter](https://gitter.im/mindfulness-at-the-computer/Lobby), #pyqt @ freenode IRC, [list](http://wiki.qt.io/Online_Communities)
SQLite through sqlite3 | - | [py module](https://docs.python.org/3/library/sqlite3.html), [official](https://www.sqlite.org/docs.html) | [Gitter](https://gitter.im/mindfulness-at-the-computer/Lobby)
[unittest + qttest](unittest-and-qttest) | | [unittest](https://docs.python.org/3/library/unittest.html) [qttest](http://doc.qt.io/qt-5/qtest.html)| [Gitter](https://gitter.im/mindfulness-at-the-computer/Lobby)

The only external dependency for the software itself is PyQt5. In general we'd like to keep the
number of external dependencies to a minimum to avoid complications


## Application structure

1. User interacts with the application
2. Qt sends signal
3. Application catches the signal (through the `connect`ed function)
   * Handler functions are named with the prefix `on_`
4. Handler function checks the `updating_gui_bool` variable and exits if `True`
5. Handler function updates the model/database
6. Handler function emits a custom signal (a `pyqtSignal` we have created ourselves)
   * Custom signals are named with the prefix `_signal`
7. Custom signal arrives in `main_win.py`
8. The `update_gui` function in `main_win.py` is called
9. This `update_gui` function in `main_win.py` then calls `update_gui` functions for its child objects
10. The `update_gui` functions set the `updating_gui_bool` variable to `True` at the start
11. The `update_gui` functions update their respective GUIs by reading data from the model/database
10. The `update_gui` functions set the `updating_gui_bool` variable to `False` at the end

Some of Qt's signals are fired only at user interaction, but often they are also fired at a programmatic change. To avoid infinite loops we set a `updating_gui_bool` when needed


## Code Conventions

These things that are different from PEP8 or standard Python recommendations:
* one class per file (plus minor supporting classes)
* 120 chars max per line

### Variable naming

Prefixes: None used at the moment

Suffixes:
* `_l[x]`, or `_wt[x]` where `wt_`/`l_` stands for widget/layout, and `[x]` is a number which describes the level of the widget or layout --- this helps us understand the structure of the application in places where there are nested layouts
* `_[type]`, for example `_int` --- this helps us be aware of type
  * For Qt the suffixes start with a `q`, for example `qpb` is short for `qPushButton`


## Automatic testing

`unittest` and `QtTest` are used for auto-testing

* [Article about auto-testing with unittest+QtTest](http://johnnado.com/pyqt-qtest-example/)
  * [Example code](https://bitbucket.org/jmcgeheeiv/pyqttestexample/src/)


## Continuous Integration

### Code coverage

For coverage.py to discover the subdirectories of the root dir specified with `--source` we need to have an `__init__.py` file for each directory/package

### Travis CI

[Python documentation](https://docs.travis-ci.com/user/languages/python/)

[We need to enable xvfb to do GUI auto-testing](https://docs.travis-ci.com/user/gui-and-headless-browsers/#Using-xvfb-to-Run-Tests-That-Require-a-GUI)


***

Also see the [technical research](https://github.com/mindfulness-at-the-computer/mindfulness-at-the-computer/wiki/Tech-Research) page on the wiki
