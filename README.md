
# Mindfulness at the Computer

A mindfulness and self-care application for people spending many hours in front of the computer

Features:
* Receive notifications to remember to be mindful of breathing
* Follow and track your breathing (in, out)
  * Breathe with text help ("Breathing in I know I am breathing in") and write your own texts
* Get reminders when it's time to take a break from the computer (and take care of your body)


## Screenshots

![Main window](docs/img/screenshot-window-1.png)

![Notification](docs/img/screenshot-notification-1.png)

![System tray](docs/img/screenshot-systray-1.png)

![Rest reminder](docs/img/screenshot-rest-reminder-1.png)

(These screenshots have been taken on a GNU/Linux system, it look a bit different for you)


## Downloads

TBD


## Installation

There are no installation packages but it's simple to install by following these steps:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip install --upgrade pip` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
4. On the command line: `pip install PyQt5` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
5. Download the project files from GitHub, by clicking on *the green "Clone or download" button* and then "Download ZIP"
6. Unzip the downloaded file

On MacOS you also need to install growl for the breathing reminder notifications to be shown

To start:

1. Change directory to where the software files have been extracted
2. Type and run `python mindfulness-at-the-computer.py` on Windows or `python3 mindfulness-at-the-computer.py`on GNU/Linux systems

### Advanced setup (optional)

Please note: *This is not necessary for running the application*

#### GNU/Linux systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - for example Gnome and KDE - you can use the bwb.desktop file included in the source (please note that if using a file manager such as the Gnome file manager you may see the name displayed as "Well-being Diary" rather than the file name) to make the application visible in any start-menu-like menu (in Lubuntu this is called the "main menu" and it's shown when clicking the button in the lower left, "vanilla" (the ordinary) Ubuntu may not have a menu like this

To use this file:

1. Edit the `mindfulness-at-the-computer.desktop` file and change the paths to match the path that you are using
2. Copy the `mindfulness-at-the-computer.desktop` file to your desktop or any place where you want to be able to start the application from
3. Copy the `mindfulness-at-the-computer.desktop` file to `/usr/share/applications/` using `sudo`


## Sign up for updates

Email list


## For developers

* Developer documentation Link: TBD
* Other projects https://fswellbeing.github.io/
* License: GPLv3


## User documentation

### Following the breath

Click the "Start" button to start following the breath

To switch between in and out breath you can use one of the following methods:

* Press the in and out buttons
  * You can press the same button again, both the in and out button will switch state
* Use the keyboard by pressing and holding down the left or right shift key to breathe in and releasing to breathe out
* Hover over the up and down buttons with the mouse cursor

#### ...with a text

If you first select a breathing phrase in the list to the left you can breathe with the text

### Rest reminders

Adding a new rest action

TBD: images

### Breathing reminders

First select a breathing phrase in the list to the left




***

Aka: m@c, matc

