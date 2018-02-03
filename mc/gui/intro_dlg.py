import logging
import mc.model
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.gui.breathing_dlg
import mc.mc_global

NEXT_STR = "Next >>"
PREV_STR = "<< Prev"
MARGIN_TOP_INT = 25
PARAGRAPH_SPACING_INT = 10


class IntroDlg(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal(bool)
    # -the boolean indicates whether or not we want the breathing dialog to open

    def __init__(self):
        super().__init__()

        self.wizard_qsw_w3 = QtWidgets.QStackedWidget()
        self.prev_qpb = QtWidgets.QPushButton(PREV_STR)
        self.next_qpb = QtWidgets.QPushButton(NEXT_STR)

        self.initUI()

    def initUI(self):
        welcome = WelcomePage()
        intro = IntroPage()
        initial_setup = BreathingInitSetupPage()
        breathing_dialog_coming = BreathingDialogComing()

        self.wizard_qsw_w3.addWidget(welcome)
        self.wizard_qsw_w3.addWidget(intro)
        self.wizard_qsw_w3.addWidget(initial_setup)
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

        self.setGeometry(300, 300, 550, 450)
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

        self.initUI()

    def initUI(self):
        title_qll = QtWidgets.QLabel("Welcome")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        text_qll = QtWidgets.QLabel(
            '<p>Welcome to Mindfulness at the Computer! '
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


class IntroPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        title_qll = QtWidgets.QLabel("How to use this wizard")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        text_qll = QtWidgets.QLabel(
            '<p>You can use this wizard to read about and set up the application.<br /> '
            'You can return to this wizard later by going to <br /> <strong>help -> show intro wizard</strong></p>'
            "<p>&nbsp;</p>"
            "<p>These are the parts of the interface:</p>"
            "<ol>"
            "<li>The breathing dialog and notifications</li>"
            "<li>The rest dialog and notifications</li>"
            '<li>The settings window <br /> (available from systray menu -> <strong>Open Settings</strong>)</li>'
            "<li>The system tray icon and menu</li>"
            "</ol>"
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


class BreathingInitSetupPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.time_overview_vbox_l3 = None
        self.grid = QtWidgets.QGridLayout()

        self.initUI()

    def initUI(self):
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

        notification_interval_qll = QtWidgets.QLabel("Time between breathing notifications")
        notification_interval_qsp = QtWidgets.QSpinBox()
        notification_interval_qsp.valueChanged.connect(self.on_time_btw_notifications_value_changed)
        notification_interval_qsp.setValue(settings.breathing_reminder_interval_int)

        breathing_interval_qll = QtWidgets.QLabel("Breathing dialog after x nr of notifications")
        breathing_interval_qsp = QtWidgets.QSpinBox()
        breathing_interval_qsp.valueChanged.connect(self.on_dlg_after_nr_notifications_value_changed)
        breathing_interval_qsp.setValue(settings.breathing_reminder_nr_before_dialog_int)

        rest_interval_qll = QtWidgets.QLabel("Rest after minutes")
        rest_interval_qsp = QtWidgets.QSpinBox()
        rest_interval_qsp.valueChanged.connect(self.on_time_before_rest_value_changed)
        rest_interval_qsp.setValue(settings.rest_reminder_interval)

        time_overview_background_qfr = QtWidgets.QFrame()
        time_overview_background_qfr.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)

        self.time_overview_vbox_l3 = QtWidgets.QVBoxLayout()
        self.time_overview_vbox_l3.setContentsMargins(12, 12, 12, 12)

        self.grid.setSpacing(10)
        self.grid.addWidget(title_qll, 1, 0, 1, 3)
        self.grid.addWidget(intro_qll, 2, 0, 1, 3)
        self.grid.addWidget(notification_interval_qll, 3, 0)
        self.grid.addWidget(notification_interval_qsp, 3, 1)
        self.grid.addWidget(breathing_interval_qll, 4, 0)
        self.grid.addWidget(breathing_interval_qsp, 4, 1)
        self.grid.addWidget(rest_interval_qll, 5, 0)
        self.grid.addWidget(rest_interval_qsp, 5, 1)
        self.grid.addWidget(time_overview_background_qfr, 3, 2, 3, 1)
        self.grid.addLayout(self.time_overview_vbox_l3, 3, 2, 3, 1)

        self.setLayout(self.grid)

        self.update_gui_time_overview()

    def on_time_before_rest_value_changed(self, i_new_value: int):
        logging.debug("on_time_before_rest_value_changed, i_new_value = " + str(i_new_value))
        mc.model.SettingsM.rest_reminder_interval = i_new_value
        self.update_gui_time_overview()

    def on_dlg_after_nr_notifications_value_changed(self, i_new_value: int):
        logging.debug("on_dlg_after_nr_notifications_value_changed, i_new_value = " + str(i_new_value))
        mc.model.SettingsM.update_breathing_reminder_nr_per_dialog(i_new_value)
        self.update_gui_time_overview()

    def on_time_btw_notifications_value_changed(self, i_new_value: int):
        logging.debug("on_time_btw_notifications_value_changed, i_new_value = " + str(i_new_value))
        mc.model.SettingsM.update_breathing_reminder_interval(i_new_value)
        self.update_gui_time_overview()

    def on_play_audio_toggled(self, i_checked: bool):
        mc.model.SettingsM.update_breathing_dialog_audio_active(i_checked)
        if not mc.model.SettingsM.get().breathing_reminder_audio_path_str:
            mc.model.SettingsM.update_breathing_reminder_audio_path("small_bell_long[cc0].wav")
        self.update_gui_time_overview()

    def update_gui_time_overview(self):
        if self.time_overview_vbox_l3 is None:
            return
        mc.mc_global.clear_widget_and_layout_children(self.time_overview_vbox_l3)
        settings = mc.model.SettingsM.get()
        counter_int = 0
        while True:
            counter_int += 1
            minutes_int = counter_int * settings.breathing_reminder_interval_int
            if minutes_int >= settings.rest_reminder_interval:
                break
            elif settings.breathing_reminder_nr_before_dialog_int != 0 and \
                    (counter_int % settings.breathing_reminder_nr_before_dialog_int) == 0:
                breathing_dialog_qll = QtWidgets.QLabel()
                self.time_overview_vbox_l3.addWidget(breathing_dialog_qll)
                breathing_dialog_qll.setText("Breathing dialog: " + str(minutes_int) + " minutes")
            else:
                breathing_reminder_qll = QtWidgets.QLabel()
                self.time_overview_vbox_l3.addWidget(breathing_reminder_qll)
                breathing_reminder_qll.setText("Breathing reminder: " + str(minutes_int) + " minutes")

        self.rest_time_qll = QtWidgets.QLabel()
        self.time_overview_vbox_l3.addWidget(self.rest_time_qll)
        self.rest_time_qll.setText("Rest: " + str(settings.rest_reminder_interval) + " minutes")


class BreathingDialogComing(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        title_qll = QtWidgets.QLabel("Breathing Dialog")
        title_qll.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        text_qll = QtWidgets.QLabel(
            "<p>When you click on finish and exit this wizard a breathing dialog will be shown. </p>"
            "<p><strong>Breathing in:</strong> hover over the central magenta square</p>"
            "<p><strong>Breathing out:</strong> hover over the green background</p>"
        )
        text_qll.setWordWrap(True)
        text_qll.setFont(mc.mc_global.get_font_xlarge())

        vbox_l2 = QtWidgets.QVBoxLayout()
        vbox_l2.addSpacing(MARGIN_TOP_INT)
        vbox_l2.addWidget(title_qll)
        vbox_l2.addStretch(1)
        vbox_l2.addWidget(text_qll)
        vbox_l2.addStretch(1)

        self.setLayout(vbox_l2)
