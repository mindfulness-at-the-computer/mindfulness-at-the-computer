[![GitHub (pre-)release](https://img.shields.io/github/release/SunyataZero/mindfulness-at-the-computer/all.svg)](https://github.com/SunyataZero/mindfulness-at-the-computer/releases/latest)
[![Build Status](https://travis-ci.org/SunyataZero/mindfulness-at-the-computer.svg?branch=master)](https://travis-ci.org/SunyataZero/mindfulness-at-the-computer)
[![Code Health](https://landscape.io/github/SunyataZero/mindfulness-at-the-computer/master/landscape.svg?style=flat)](https://landscape.io/github/SunyataZero/mindfulness-at-the-computer/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/799f63cfa9254d4b9c3b1f93eebac994)](https://www.codacy.com/app/SunyataZero/mindfulness-at-the-computer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SunyataZero/mindfulness-at-the-computer&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/SunyataZero/mindfulness-at-the-computer/branch/master/graph/badge.svg)](https://codecov.io/gh/SunyataZero/mindfulness-at-the-computer)

# Mindfulness at the Computer

*This file is written for nerds and developers who want to contribute to the project, for an intro to the application please check out the [**application website**](https://sunyatazero.github.io/mindfulness-at-the-computer/)*

<!-- TBD: If you are a user you can find the user guide here -->

## Running from Source

If there isn't a download for your platform (see the downloads section above) you can instead start the application by following these steps:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip install --upgrade pip` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
4. On the command line: `pip install PyQt5` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
5. Download the project files from GitHub, by clicking on *the green "Clone or download" button* and then "Download ZIP"
6. Unzip the downloaded file
7. Change directory to where the software files have been extracted
8. Type and run `python mindfulness-at-the-computer.py` on Windows or `python3 mindfulness-at-the-computer.py`on GNU/Linux systems

On MacOS you also need to install growl for the breathing reminder notifications to be shown


### Advanced Setup (Optional)

Please note: *This is not necessary for running the application*

#### GNU/Linux Systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - for example Gnome and KDE - you can use the bwb.desktop file included in the source (please note that if using a file manager such as the Gnome file manager you may see the name displayed as "Well-being Diary" rather than the file name) to make the application visible in any start-menu-like menu (in Lubuntu this is called the "main menu" and it's shown when clicking the button in the lower left, "vanilla" (the ordinary) Ubuntu may not have a menu like this

To use this file:

1. Edit the `mindfulness-at-the-computer.desktop` file and change the paths to match the path that you are using
2. Copy the `mindfulness-at-the-computer.desktop` file to your desktop or any place where you want to be able to start the application from
3. Copy the `mindfulness-at-the-computer.desktop` file to `/usr/share/applications/` using `sudo`

## Social

[Gitter chat](https://gitter.im/mindfulness-at-the-computer/Lobby)

## License

GPLv3

## Varia

* Developer documentation Link: TBD
* Other projects https://fswellbeing.github.io/

## Installation

See [Running from Source](#running-from-source) above

<!--
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/mindfulness-at-the-computer/Lobby)
[![saythanks](https://img.shields.io/badge/say-thanks-98e633.svg)](https://saythanks.io/to/SunyataZero)
[![license-gplv3](https://img.shields.io/badge/license-GPLv3-a42e2b.svg)](https://www.gnu.org/licenses/gpl.html)

Aka: m@c, matc
-->

