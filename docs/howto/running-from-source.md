
# Running from Source

If you don't see a download option for the platform of your choice, or you just prefer running from source for other reasons, you can follow these steps to start the application:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip install --upgrade pip` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
4. On the command line: `pip install PyQt5` (On Ubuntu use `sudo -H` and `pip3` instead of `pip`)
5. Download the project files from GitHub, by clicking on *the green "Clone or download" button* and then "Download ZIP"
6. Unzip the downloaded file
7. Change directory to where the software files have been extracted
8. Type and run `python mindfulness-at-the-computer.py` on Windows or `python3 mindfulness-at-the-computer.py`on GNU/Linux systems

NOTE:
If you are running **MacOS** you need to install growl to get the breathing reminder notifications.

## Creating a shortcut (Optional)

### Windows

You can create a shortcut by right clicking the .exe file for the application and choosing "Send to" and then "Desktop (create shortcut)"

### GNU/Linux Systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - such as Gnome and KDE - you can use the bwb.desktop file included in the source (If using a file manager, such as Gnome File Manager, you may see the name displayed as "Well-being Diary" rather than "bwb.desktop") to make the application visible in any start-menu-like menu. In Lubuntu, this is called the "main menu" and it's shown when the button in the lower left is clicked. "Vanilla" Ubuntu (ordinary) may not have a menu like this.

To use this file:

1. Edit the `mindfulness-at-the-computer.desktop` file (from the varia/ directory) and change the paths to match the path that you are using
2. Copy the `mindfulness-at-the-computer.desktop` file to your desktop or to any place from where you want to be able to start the application
3. Copy the `mindfulness-at-the-computer.desktop` file to `/usr/share/applications/` using `sudo`
