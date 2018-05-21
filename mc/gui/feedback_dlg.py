import logging
import mc.model
import webbrowser
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import mc.gui.breathing_dlg
import mc.gui.breathing_notification
import mc.gui.rest_notification
import mc.gui.rest_dlg
import mc.mc_global


class FeedbackDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)

        help_request_str = """
<h3>Help Us</h3>
<p>We are grateful for feedback, for example please contact us if you</p>
<ul>
<li>find a bug</li>
<li>have a suggestion for a new feature</li>
<li>have ideas for how to improve the interface</li>
<li>have feedback about what you like about the application and how it helps you when using the computer (we are looking for testimonials!)</li>
</ul>
<p>You can reach us using this email address:</p>"""

        help_request_qll = QtWidgets.QLabel()
        # help_request_qll.setFont(mc.mc_global.get_font_large())
        help_request_qll.setText(help_request_str)
        help_request_qll.setWordWrap(True)
        vbox_l2.addWidget(help_request_qll)

        email_qll = QtWidgets.QLabel()
        email_qll.setFont(mc.mc_global.get_font_xxlarge())
        email_qll.setText('sunyata.software@gmail.com')
        vbox_l2.addWidget(email_qll)

        # Doesn't work on Sunyata's system (not through python or qt):
        """
        emailus_qpb = QtWidgets.QPushButton("Email us!")
        emailus_qpb.clicked.connect(self.on_emailus_clicked)
        vbox_l2.addWidget(emailus_qpb)
        """

        self.show_again_qcb = QtWidgets.QCheckBox("Show this dialog at startup again in the future")
        self.show_again_qcb.toggled.connect(self.on_show_again_toggled)
        vbox_l2.addWidget(self.show_again_qcb)

        self.update_gui()

        self.show()

    def update_gui(self):
        self.gui_update_bool = True
        settings = mc.model.SettingsM.get()
        self.show_again_qcb.setChecked(
            settings.nr_times_started_since_last_feedback_notif != mc.mc_global.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP
        )
        self.gui_update_bool = False

    def on_show_again_toggled(self, i_checked: bool):
        if self.gui_update_bool:
            return
        settings = mc.model.SettingsM.get()
        if i_checked:
            if settings.nr_times_started_since_last_feedback_notif == mc.mc_global.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP:
                settings.nr_times_started_since_last_feedback_notif = 0
            else:
                pass
        else:
            settings.nr_times_started_since_last_feedback_notif = mc.mc_global.FEEDBACK_DIALOG_NOT_SHOWN_AT_STARTUP

    def on_emailus_clicked(self):
        url_string = "mailto:?to=sunyata.software@gmail.com?Subject=Feedback"

        # url = QtCore.QUrl(url_string)
        # QtGui.QDesktopServices.openUrl(url)

        webbrowser.open(url_string)
