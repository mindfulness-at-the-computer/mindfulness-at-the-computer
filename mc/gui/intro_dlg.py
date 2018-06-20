import logging
import mc.model
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.gui.breathing_dlg
import mc.gui.breathing_notification
import mc.gui.rest_notification
import mc.gui.rest_dlg
from mc.gui.timing_settings_wt import TimingOverviewWt
from mc.model import SettingsM
import mc.mc_global

NEXT_STR = "Next >>"
PREV_STR = "<< Prev"
MARGIN_TOP_INT = 35
PARAGRAPH_SPACING_INT = 10


class IntroDlg(QtWidgets.QDialog):
    """
    The introduction wizard with examples of dialogs and functionality to adjust initial settings
    """
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        self.prev_qpb = QtWidgets.QPushButton(PREV_STR)
        self.next_qpb = QtWidgets.QPushButton(NEXT_STR)

        self.initial_setup = TimingInitSetupPage()
        self._init_ui()

    def _init_ui(self):
        welcome = WelcomePage()
        system_tray = SystemTrayPage()
        breathing_notification = BreathingNotificationPage()
        breathing_dialog = BreathingDialogPage()
        breathing_dialog_coming = BreathingDialogComing()

        self.wizard_qsw_w3.addWidget(welcome)
        self.wizard_qsw_w3.addWidget(system_tray)
        self.wizard_qsw_w3.addWidget(breathing_notification)
        self.wizard_qsw_w3.addWidget(breathing_dialog)
        self.wizard_qsw_w3.addWidget(self.initial_setup)
        self.wizard_qsw_w3.addWidget(breathing_dialog_coming)

        self.prev_qpb.clicked.connect(self.on_prev_clicked)
        self.next_qpb.clicked.connect(self.on_next_clicked)

        hbox_l3 = QtWidgets.QHBoxLayout()
        hbox_l3.addStretch(1)
        hbox_l3.addWidget(self.prev_qpb, stretch=1)
        hbox_l3.addWidget(self.next_qpb, stretch=1)
        hbox_l3.addStretch(1)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addWidget(self.wizard_qsw_w3)
        vbox_l2.addLayout(hbox_l3)

        self.setGeometry(300, 150, 650, 500)
        self.setLayout(vbox_l2)
        self.update_gui()
        self.show()

    def on_next_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int >= self.wizard_qsw_w3.count() - 1:
            self.close_signal.emit(True)
            self.close()
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int + 1)
        self.update_gui()

    def on_prev_clicked(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        if current_index_int <= 0:
            return
        logging.debug("current_index_int = " + str(current_index_int))
        self.wizard_qsw_w3.setCurrentIndex(current_index_int - 1)
        self.update_gui()

    def update_gui(self):
        current_index_int = self.wizard_qsw_w3.currentIndex()
        self.prev_qpb.setDisabled(current_index_int == 0)

        if current_index_int == self.wizard_qsw_w3.count() - 1:
            self.next_qpb.setText("Finish")  # "open breathing dialog"
        else:
            self.next_qpb.setText(NEXT_STR)


class WelcomePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        title_qll = QtWidgets.QLabel("Welcome")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        text_qll = QtWidgets.QLabel(
            "<p>Welcome to Mindfulness at the Computer!</p>"
            "<p>This application reminds you to stay aware of your breathing and to take breaks.</p>"
        )
        text_qll.setWordWrap(True)
        text_qll.setFont(mc.mc_global.get_font_xlarge())

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addSpacing(MARGIN_TOP_INT)
        vbox_l2.addWidget(title_qll)
        vbox_l2.addStretch(1)
        vbox_l2.addWidget(text_qll)
        vbox_l2.addSpacing(PARAGRAPH_SPACING_INT)
        vbox_l2.addStretch(1)

        self.setLayout(vbox_l2)


class SystemTrayPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        title_qll = QtWidgets.QLabel("The system tray")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))
        title_qll.setAlignment(QtCore.Qt.AlignHCenter)

        description_qll = QtWidgets.QLabel(
            "When you run Mindfulness at the computer it is accessible via the system tray. "
            "From the menu that opens when clicking on this icon "
            "you can adjust settings or invoke a breathing or rest session"
        )
        description_qll.setWordWrap(True)
        description_qll.setFont(mc.mc_global.get_font_xlarge())

        system_tray_qll = QtWidgets.QLabel()
        system_tray_qll.setPixmap(QtGui.QPixmap(mc.mc_global.get_app_icon_path("icon-br.png")))
        system_tray_qll.setAlignment(QtCore.Qt.AlignHCenter)

        vbox_l3 = QtWidgets.QVBoxLayout()
        vbox_l3.addSpacing(MARGIN_TOP_INT)
        vbox_l3.addWidget(title_qll)
        vbox_l3.addStretch(1)
        vbox_l3.addWidget(description_qll)
        vbox_l3.addStretch(1)
        vbox_l3.addWidget(system_tray_qll)
        vbox_l3.addStretch(1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        hbox_l2.addStretch(1)
        hbox_l2.addLayout(vbox_l3)
        hbox_l2.addStretch(1)

        self.setLayout(hbox_l2)


class BreathingNotificationPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        title_qll = QtWidgets.QLabel("The breathing notification")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))
        title_qll.setAlignment(QtCore.Qt.AlignHCenter)

        description_qll = QtWidgets.QLabel(
            "This notification pops up every once in a while. "
            "You can adjust how often you would like to get notified. "
            "If you like, you can start a breathing session from here"
        )
        description_qll.setWordWrap(True)
        description_qll.setFont(mc.mc_global.get_font_xlarge())

        breathing_notification = mc.gui.breathing_notification.BreathingNotification()
        breathing_notification.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        breathing_notification.breathe_qpb.setDisabled(True)

        vbox_l3 = QtWidgets.QVBoxLayout()
        vbox_l3.addSpacing(MARGIN_TOP_INT)
        vbox_l3.addWidget(title_qll)
        vbox_l3.addStretch(1)
        vbox_l3.addWidget(description_qll)
        vbox_l3.addStretch(1)
        vbox_l3.addWidget(breathing_notification)
        vbox_l3.addStretch(1)

        hbox_l2 = QtWidgets.QHBoxLayout()
        hbox_l2.addStretch(1)
        hbox_l2.addLayout(vbox_l3)
        hbox_l2.addStretch(1)

        self.setLayout(hbox_l2)


class BreathingDialogPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        title_qll = QtWidgets.QLabel("The breathing dialog")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))
        title_qll.setAlignment(QtCore.Qt.AlignHCenter)

        description_qll = QtWidgets.QLabel(
            "This dialog helps you to relax and return to your breathing. "
            "Try it out, it is interactive!"
        )
        description_qll.setWordWrap(True)
        description_qll.setFont(mc.mc_global.get_font_xlarge())

        breathing_dlg = mc.gui.breathing_dlg.BreathingDlg()
        breathing_dlg.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        breathing_dlg._close_qpb.setDisabled(True)

        vbox_l3 = QtWidgets.QVBoxLayout()
        vbox_l3.addSpacing(MARGIN_TOP_INT)
        vbox_l3.addWidget(title_qll)
        vbox_l3.addWidget(description_qll)
        vbox_l3.addStretch(1)
        vbox_l3.addWidget(breathing_dlg)
        vbox_l3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        hbox_l2 = QtWidgets.QHBoxLayout()
        hbox_l2.addStretch(1)
        hbox_l2.addLayout(vbox_l3)
        hbox_l2.addStretch(1)

        self.setLayout(hbox_l2)


class TimingInitSetupPage(QtWidgets.QWidget):
    rest_settings_updated_from_intro_signal = QtCore.pyqtSignal(str)
    breathing_settings_updated_from_intro_signal = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.updating_gui_bool = False

        self.overview_qlw = TimingOverviewWt()
        self.grid = QtWidgets.QGridLayout()
        self.notification_interval_qsp = QtWidgets.QSpinBox()
        self.show_after_qsb = QtWidgets.QSpinBox()
        self.rest_interval_qsp = QtWidgets.QSpinBox()

        self._init_ui()
        self.update_gui()
        self._connect_slots_to_signals()

    def _init_ui(self):
        settings = mc.model.SettingsM.get()

        title_qll = QtWidgets.QLabel("Initial setup")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        intro_qll = QtWidgets.QLabel(
            "<p>Please select the initial setup parameters for the breathing dialog. "
            "It's possible to change the values later on using the settings window "
            '(available from the systray menu -> <strong>Open Settings</strong>).</p>'
        )
        intro_qll.setWordWrap(True)
        intro_qll.setFont(mc.mc_global.get_font_xlarge())

        header_qll = QtWidgets.QLabel("Time overview")
        header_qll.setFont(mc.mc_global.get_font_medium(i_bold=True))
        header_qll.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)

        notification_interval_qll = QtWidgets.QLabel("Time between breathing notifications")
        self.notification_interval_qsp.setValue(settings.breathing_reminder_interval_int)
        self.notification_interval_qsp.setMinimum(1)

        breathing_interval_qll = QtWidgets.QLabel("Breathing dialog after x nr of notifications")
        self.show_after_qsb.setValue(settings.breathing_reminder_nr_before_dialog_int)

        rest_interval_qll = QtWidgets.QLabel("Rest after minutes")
        self.rest_interval_qsp.setValue(settings.rest_reminder_interval)

        self.time_overview_vbox_l3 = QtWidgets.QVBoxLayout()
        self.time_overview_vbox_l3.setContentsMargins(12, 12, 12, 12)

        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(20)
        self.grid.addWidget(title_qll, 1, 0, 1, 3)
        self.grid.addWidget(intro_qll, 2, 0, 1, 3)
        self.grid.addWidget(header_qll, 3, 2)

        self.grid.addWidget(notification_interval_qll, 5, 0)
        self.grid.addWidget(self.notification_interval_qsp, 5, 1)
        self.grid.addWidget(self.overview_qlw, 4, 2, 5, 1)
        self.grid.addWidget(breathing_interval_qll, 6, 0)
        self.grid.addWidget(self.show_after_qsb, 6, 1)
        self.grid.addWidget(rest_interval_qll, 7, 0)
        self.grid.addWidget(self.rest_interval_qsp, 7, 1)

        self.setLayout(self.grid)

        self.overview_qlw.update_gui_time_overview()

    def update_gui(self):
        self.updating_gui_bool = True

        settings = mc.model.SettingsM.get()
        self.notification_interval_qsp.setValue(settings.breathing_reminder_interval_int)
        self.show_after_qsb.setValue(settings.breathing_reminder_nr_before_dialog_int)
        self.rest_interval_qsp.setValue(settings.rest_reminder_interval_int)

        self.updating_gui_bool = False

    def _connect_slots_to_signals(self):
        self.notification_interval_qsp.valueChanged.connect(self.on_time_btw_notifications_value_changed)
        self.show_after_qsb.valueChanged.connect(self.on_dlg_after_nr_notifications_value_changed)
        self.rest_interval_qsp.valueChanged.connect(self.on_time_before_rest_value_changed)

    def on_time_btw_notifications_value_changed(self, i_new_value: int):
        logging.debug("on_time_btw_notifications_value_changed, i_new_value = " + str(i_new_value))
        SettingsM.update_breathing_reminder_interval(i_new_value)
        self.overview_qlw.update_gui_time_overview()
        self.breathing_settings_updated_from_intro_signal.emit('intro')

    def on_dlg_after_nr_notifications_value_changed(self, i_new_value: int):
        logging.debug("on_dlg_after_nr_notifications_value_changed, i_new_value = " + str(i_new_value))
        SettingsM.update_breathing_reminder_nr_per_dialog(i_new_value)
        self.overview_qlw.update_gui_time_overview()
        self.breathing_settings_updated_from_intro_signal.emit('intro')

    def on_time_before_rest_value_changed(self, i_new_value: int):
        logging.debug("on_time_before_rest_value_changed, i_new_value = " + str(i_new_value))
        SettingsM.update_rest_reminder_interval(i_new_value)
        self.overview_qlw.update_gui_time_overview()
        self.rest_settings_updated_from_intro_signal.emit('intro')


class BreathingDialogComing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()

    def _init_ui(self):
        title_qll = QtWidgets.QLabel("Finish")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        text_qll = QtWidgets.QLabel(
            "<p>When you click on finish and exit this wizard a breathing dialog will be shown. </p>"
            "<p><strong>Breathing in:</strong> Hover over the green box</p>"
            "<p><strong>Breathing out:</strong> Hover outside the green box</p>"
        )
        text_qll.setWordWrap(True)
        text_qll.setFont(mc.mc_global.get_font_xlarge())

        relaunch_wizard_qll = QtWidgets.QLabel(
            '<p>You can start this wizard again by choosing "Help" -> "Show intro wizard" in the settings '
            'window (available from the system tray icon menu)</p>'
        )
        relaunch_wizard_qll.setWordWrap(True)
        relaunch_wizard_qll.setFont(mc.mc_global.get_font_medium())
        relaunch_wizard_qll.setAlignment(QtCore.Qt.AlignCenter)

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addSpacing(MARGIN_TOP_INT)
        vbox_l2.addWidget(title_qll)
        vbox_l2.addStretch(3)
        vbox_l2.addWidget(text_qll)
        vbox_l2.addStretch(3)
        vbox_l2.addWidget(relaunch_wizard_qll)
        vbox_l2.addStretch(1)

        self.setLayout(vbox_l2)
