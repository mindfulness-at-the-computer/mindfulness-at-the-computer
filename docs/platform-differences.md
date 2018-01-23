
### Behavior at application error

Windows: When an error is encountered, the application will crash

Linux-based: The application just prints to stdout

### Notifications

Some systems do not show notifications

For example, older versions of MacOS seem to have this problem. In such a case, the user will need to install growl

### Systray

Some systems do not have a system tray

XFCE: Left clicking icon in system tray does nothing

### Minimize area

Systems that lack a minimizing area

### 64 and 32 bit Linux-based systems

Application binaries must be built on the same bit-numbered system as the OS where they will run. This may be because of glibc

### Virtual desktop and multiple desktops, etc

First some definitions:
* Multiple desktops: A computer with more than one graphics card (or a graphics card with several physical outputs) can have multiple desktops
  * Virtual desktop: A computer with multiple desktops (see above) and where the user has chosen to set up the system so that it seems like everything is on one long desktop
* (unknown what word to use): A computer where the OS provides several different desktops that the user can switch between (on LXDE called the "desktop pager"). Please note that this isn't called "virtual desktops" even though this would be natural

Multiple desktops and virtual desktops are covered here: http://doc.qt.io/qt-5/qdesktopwidget.html
