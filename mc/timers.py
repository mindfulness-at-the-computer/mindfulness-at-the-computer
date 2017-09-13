from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.model
import mc.mc_global
import mc.dlg.rest_reminder_dialog

class RestTimer:
    def __init__(self):
        pass

    def stop_rest_reminder_timer(self):
        if self.rest_reminder_qtimer is not None and self.rest_reminder_qtimer.isActive():
            self.rest_reminder_qtimer.stop()
        self.rest_settings_widget.update_gui()  # -so that the progressbar is updated

    def start_rest_reminder_timer(self):
        if mc.model.SettingsM.get().rest_reminder_active_bool:
            return
        mc.mc_global.rest_reminder_minutes_passed_int = 0
        self.stop_rest_reminder_timer()
        self.rest_reminder_qtimer = QtCore.QTimer(self)
        self.rest_reminder_qtimer.timeout.connect(self.rest_reminder_timeout)
        self.rest_reminder_qtimer.start(60 * 1000)  # -one minute


    def rest_reminder_timeout(self):
        mc.mc_global.rest_reminder_minutes_passed_int += 1
        rest_reminder_interval_minutes_int = mc.model.SettingsM.get().rest_reminder_interval_int
        if mc.mc_global.rest_reminder_minutes_passed_int >= rest_reminder_interval_minutes_int:
            self.show_rest_reminder()
        self.rest_settings_widget.rest_reminder_qprb.setValue(
            mc.mc_global.rest_reminder_minutes_passed_int
        )


    def show_rest_reminder(self):
        mc.mc_global.rest_reminder_minutes_passed_int = 0

        rest_reminder = mc.dlg.rest_reminder_dialog.RestReminderDialog(self)
        result = rest_reminder.exec()
        if result:
            outcome_int = rest_reminder.dialog_outcome_int
            if outcome_int != mc.dlg.rest_reminder_dialog.CLOSED_RESULT_INT:
                total_time = mc.model.SettingsM.get().rest_reminder_interval_int
                mc.mc_global.rest_reminder_minutes_passed_int = total_time - rest_reminder.dialog_outcome_int
            else:
                pass
        self.update_gui()


    def on_breathing_settings_updated(self):
        settings = mc.model.SettingsM.get()
        if settings.breathing_reminder_active_bool:
            self.start_breathing_notification_timer()
        else:
            self.stop_breathing_notification_timer()


    def stop_breathing_notification_timer(self):
        if self.breathing_qtimer is not None and self.breathing_qtimer.isActive():
            self.breathing_qtimer.stop()


    def start_breathing_notification_timer(self):
        if not mc.model.SettingsM.get().breathing_reminder_active_bool:
            return
        self.stop_breathing_notification_timer()
        settings = mc.model.SettingsM.get()
        self.breathing_qtimer = QtCore.QTimer(self)  # -please remember to send "self" to the timer
        self.breathing_qtimer.timeout.connect(self.show_breathing_notification)
        self.breathing_qtimer.start(settings.breathing_reminder_interval_int * 1000)


    def show_breathing_notification(self):
        settings = mc.model.SettingsM.get()
        if mc.mc_global.active_phrase_id_it != mc.mc_global.NO_PHRASE_SELECTED_INT:
            active_phrase = mc.model.PhrasesM.get(mc.mc_global.active_phrase_id_it)
            reminder_str = active_phrase.ib_str + "\n" + active_phrase.ob_str
            self.tray_icon.showMessage(
                "Mindful breathing",
                reminder_str.strip(),
                icon=QtWidgets.QSystemTrayIcon.NoIcon,
                msecs=settings.breathing_reminder_length_int * 1000
            )
            # TODO: The title (now "application title string") and the icon
            # could be used to show if the message is a mindfulness of breathing message
            # or a message for taking a break (or something else)

class RestTimer:
    def __init__(self):
        pass

