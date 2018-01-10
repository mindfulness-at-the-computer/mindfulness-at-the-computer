
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
