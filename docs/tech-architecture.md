
Also see the [technical research](https://github.com/SunyataZero/mindfulness-at-the-computer/wiki/Technical-Research) page on the wiki

# Tech architecture

## Dependencies

### Python 3

At the time of writing we are using Python 3.6

### Qt and PyQt 5.9

The Qt and PyQt versions seems to almost always be the same

Can be installed in different ways (pip on all systems, apt-get on Debian based systems, (install .exe file on Windows?))

## Python modules
(Part of the standard library)

### sqlite3

## Application structure

### update_gui() function

### model and database

## Code Conventions

Here are some things that are different from PEP8:
* one class per file (plus minor supporting classes)
* 120 chars max per line
* PyQt special: Upper case characters in some places

If you are using Pycharm you will get some

### Variable naming

`_lx` where `x` describes the level of the widget or layout


### Continuous Integration

Travis

https://blog.ionelmc.ro/2014/05/25/python-packaging/

https://github.com/codecov/example-python


### Code coverage --- Not relevant at the moment

for coverage.py to discover the subdirectories of the root dir specified with --source
we need to have an __init__.py file for each directory/package

https://github.com/audreyr/how-to/blob/master/python/use_coverage_with_unittest.rst


### Tests --- Not relevant at the moment

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

