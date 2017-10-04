[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/mindfulness-at-the-computer/Lobby)
[![First-timers only](https://img.shields.io/badge/first--timers--only-friendly-blue.svg)](http://www.firsttimersonly.com/)
[![GitHub (pre-)release](https://img.shields.io/github/release/SunyataZero/mindfulness-at-the-computer/all.svg)](https://github.com/SunyataZero/mindfulness-at-the-computer/releases/latest)
[![Build Status](https://travis-ci.org/SunyataZero/mindfulness-at-the-computer.svg?branch=master)](https://travis-ci.org/SunyataZero/mindfulness-at-the-computer)
[![Code Health](https://landscape.io/github/SunyataZero/mindfulness-at-the-computer/master/landscape.svg?style=flat)](https://landscape.io/github/SunyataZero/mindfulness-at-the-computer/master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/799f63cfa9254d4b9c3b1f93eebac994)](https://www.codacy.com/app/SunyataZero/mindfulness-at-the-computer?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SunyataZero/mindfulness-at-the-computer&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/SunyataZero/mindfulness-at-the-computer/branch/master/graph/badge.svg)](https://codecov.io/gh/SunyataZero/mindfulness-at-the-computer)

# Mindfulness at the Computer

This application reminds you to take breaks from the computer, helps you
remember to stay in touch with and be mindful of your breathing and body
while sitting at the computer, and helps you concentrate on breathing
in and out when you need a breathing pause.

Written in python, this application can be run on Windows and GNU/Linux

## Download

The [**application website**](https://sunyatazero.github.io/mindfulness-at-the-computer/)
includes more information (Downloads, screenshots, mailing list).

<!-- TBD: If you are a user you can find the user guide here -->

## License

GPLv3

## Social (Support and Development)

[Gitter chat](https://gitter.im/mindfulness-at-the-computer/Lobby)

## Developer document

All docs are in [this directory](docs/)

Some important documents:
* [CONTRIBUTING](CONTRIBUTING.md)
* [Technical Architecture](docs/tech-architecture.md)

## Running from Source

If you don't see a download option for the platform of your choice, follow these steps to start the application:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip install --upgrade pip` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
4. On the command line: `pip install PyQt5` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
5. Download the project files from GitHub, by clicking on *the green "Clone or download" button* and then "Download ZIP"
6. Unzip the downloaded file
7. Change directory to where the software files have been extracted
8. Type and run `python mindfulness-at-the-computer.py` on Windows or `python3 mindfulness-at-the-computer.py`on GNU/Linux systems

NOTE:
If you are on the **MacOS**, you need to install growl to get the breathing reminder notifications.

### Advanced Setup (Optional)

Please note: *This is not necessary for running the application*

#### GNU/Linux Systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - such as Gnome and KDE - you can use the bwb.desktop file included in the source (If using a file manager, such as Gnome File Manager, you may see the name displayed as "Well-being Diary" rather than "bwb.desktop") to make the application visible in any start-menu-like menu. In Lubuntu, this is called the "main menu" and it's shown when the button in the lower left is clicked. "Vanilla" Ubuntu (ordinary) may not have a menu like this.

To use this file:

1. Edit the `mindfulness-at-the-computer.desktop` file and change the paths to match the path that you are using
2. Copy the `mindfulness-at-the-computer.desktop` file to your desktop or any place where you want to be able to start the application from
3. Copy the `mindfulness-at-the-computer.desktop` file to `/usr/share/applications/` using `sudo`

## Varia

* Other projects for well-being: https://fswellbeing.github.io/


<!--
[![saythanks](https://img.shields.io/badge/say-thanks-98e633.svg)](https://saythanks.io/to/SunyataZero)
[![license-gplv3](https://img.shields.io/badge/license-GPLv3-a42e2b.svg)](https://www.gnu.org/licenses/gpl.html)

Aka: m@c, matc
-->

