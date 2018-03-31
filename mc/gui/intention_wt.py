from PyQt5 import QtWidgets, QtCore

import mc.mc_global
from mc.gui.list_view_buttons import ListViewButtons


class IntentionForm(QtWidgets.QFrame):
    """
    A form using a QDataWidgetMapper and a QSqlTableModel
    """
    def __init__(self, model, parent=None):
        super(IntentionForm, self).__init__(parent)

        self.model = model
        self.mapper = QtWidgets.QDataWidgetMapper(self)
        self.vertical_order = QtWidgets.QLineEdit()
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(400, 300, 400, 100)
        self.setWindowFlags(
            QtCore.Qt.Dialog
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
        )

        text_label = QtWidgets.QLabel(self.tr("It is my intention to:"))
        text_edit = QtWidgets.QLineEdit()

        cancel_qpb = QtWidgets.QPushButton(self.tr("Cancel"))
        cancel_qpb.clicked.connect(self.close)

        submit_qpb = QtWidgets.QPushButton(self.tr("Submit"))
        submit_qpb.clicked.connect(self._submit_form)

        self.mapper.setModel(self.model)
        self.mapper.addMapping(self.vertical_order, 1)
        self.mapper.addMapping(text_edit, 2)
        self.mapper.setSubmitPolicy(QtWidgets.QDataWidgetMapper.ManualSubmit)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(text_label, 0, 0, 1, 2)
        layout.addWidget(text_edit, 1, 0, 1, 2)
        layout.addWidget(cancel_qpb, 2, 0, 1, 1)
        layout.addWidget(submit_qpb, 2, 1, 1, 1)
        self.setLayout(layout)

        self.mapper.toFirst()

    def _submit_form(self):
        self.mapper.submit()
        self.close()


class IntentionWidget(QtWidgets.QWidget):
    def __init__(self, model, parent=None):
        super(IntentionWidget, self).__init__(parent)

        self.model = model
        self.intentions_qlv = QtWidgets.QListView()
        self.intention_form_qwt = IntentionForm(self.model)
        self.list_view_buttons = ListViewButtons(self.model, self.intentions_qlv, self.intention_form_qwt)
        self.intention_vbox_l1 = QtWidgets.QVBoxLayout()
        self.intention_hbox_l2 = QtWidgets.QHBoxLayout()
        self._init_ui()

    def _init_ui(self):
        self.setGeometry(300, 100, 600, 400)
        self.intentions_qlv.setModel(self.model)
        self.intentions_qlv.setModelColumn(2)
        self.setStyleSheet(
            "selection-background-color:" + mc.mc_global.MC_LIGHT_GREEN_COLOR_STR + ";"
            "selection-color:#000000;"
        )

        intentions_qlb = QtWidgets.QLabel(self.tr("My intentions"))
        intentions_qlb.setFont(mc.mc_global.get_font_xxlarge(i_bold=True))

        intentions_explanation_qlb = QtWidgets.QLabel(self.tr(
            "Your intentions help you to be more committed to living a mindful life.<br />"
            "You could for instance have the following intention:<br /><br />"
            "<i>Today it is my intention to take good care of myself by taking frequent breaks.</i><br />"
        ))
        intentions_explanation_qlb.setFont(mc.mc_global.get_font_xlarge())

        close_qpb = QtWidgets.QPushButton(self.tr("Close"))
        close_qpb.clicked.connect(self.close)

        self.intention_vbox_l1.addWidget(intentions_qlb)
        self.intention_vbox_l1.addWidget(intentions_explanation_qlb)
        self.intention_vbox_l1.addWidget(self.intentions_qlv)

        self.intention_hbox_l2.addLayout(self.list_view_buttons)
        self.intention_hbox_l2.addStretch(1)
        self.intention_hbox_l2.addWidget(close_qpb)
        self.intention_vbox_l1.addLayout(self.intention_hbox_l2)
        self.intention_vbox_l1.addStretch(1)

        self.setLayout(self.intention_vbox_l1)
