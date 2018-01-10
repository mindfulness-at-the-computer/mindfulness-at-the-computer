
# Manual testing

This document contains test cases for manual testing

For all the tests below: Please start the application in debug mode, or at least in such a way that you can see the debug output (from the logging)

Test Record: Please use [the wiki](https://github.com/mindfulness-at-the-computer/mindfulness-at-the-computer/wiki)

"TBD" in this document often means that the test case is yet to be written


## System Tray Menu

1. Click on the system tray icon.        
2. Click on "take break now".
3. Verify: Rest dialog comes up.

## Rest Dialog

TBD: Verify that only one rest dialog appears if multiple are "passed"

### Rest actions

1. Click on an action with an associated image in the rest dialog.
2. Verify: The image is shown.
3. Click on an action without an associated image in the rest dialog.
4. Verify: The associated text is shown.

### Waiting

1. Click the wait button (letting the wait time be at 1).
2. Verify: In the main interface the remaining time is shown as 1.
3. Verify: In the system tray menu the remaining time is almost nothing (might be shown as nothing because of rounding).
4. Wait one minute for the dialog to be shown again.
5. Verify: The dialog is shown.
6. Change the wait time value to 5.
7. Verify: In the main interface the remaining time is shown as 5.
8. Verify: In the system tray menu the remaining time is shown as the percentage you would expect (e.g. if rest interval is 20 minutes we would expect 75% of the systray progress bar to be filled).



### Broken link

TBD: Removing an image file to create a "broken link"


## Phrases

1. Select a phrase from the list to the left.
2. Verify: The breathing area text is changed.
3. Enable breathing reminders.
4. Click on "test" for the breathing reminders (or wait for the next reminder).
5. Verify: The text has been changed from before.
