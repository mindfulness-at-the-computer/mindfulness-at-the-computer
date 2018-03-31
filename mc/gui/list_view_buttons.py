from PyQt5 import QtGui

from PyQt5.QtWidgets import QHBoxLayout, QPushButton

import mc.mc_global
from mc.model import MoveDirectionEnum


class ListViewButtons(QHBoxLayout):
    def __init__(self, model, view, form, parent=None):
        super(ListViewButtons, self).__init__(parent)
        self.model = model
        self.view = view
        self.form = form
        self._init_ui()

    def _init_ui(self):
        edit_qpb = QPushButton()
        edit_qpb.clicked.connect(self.on_edit_clicked)
        edit_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("pencil-2x.png")))
        edit_qpb.setToolTip(self.tr("Edit the intention"))

        add_qpb = QPushButton(self.tr('+'))
        add_qpb.clicked.connect(self.on_add_clicked)

        remove_qpb = QPushButton()
        remove_qpb.clicked.connect(self.on_remove_clicked)
        remove_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("trash-2x.png")))
        remove_qpb.setToolTip(self.tr("Delete the selected intention"))

        move_up_qpb = QPushButton()
        move_up_qpb.clicked.connect(self.on_move_up_clicked)
        move_up_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-top-2x.png")))
        move_up_qpb.setToolTip(self.tr("Move the selected intention up"))

        move_down_qpb = QPushButton()
        move_down_qpb.clicked.connect(self.on_move_down_clicked)
        move_down_qpb.setIcon(QtGui.QIcon(mc.mc_global.get_icon_path("arrow-bottom-2x.png")))
        move_down_qpb.setToolTip(self.tr("Move the selected intention down"))

        self.view.doubleClicked.connect(self.on_edit_clicked)

        self.addWidget(add_qpb)
        self.addWidget(edit_qpb)
        self.addWidget(remove_qpb)
        self.addWidget(move_up_qpb)
        self.addWidget(move_down_qpb)

    def on_edit_clicked(self):
        self.form.show()

        if self.view.selectedIndexes():
            self.form.mapper.setCurrentIndex(self.view.selectedIndexes()[0].row())
        else:
            self.on_add_clicked()

    def on_add_clicked(self):
        row_nr = self.model.rowCount()
        vertical_order = row_nr + 1
        self.model.insertRow(row_nr)
        self.form.vertical_order.setText(str(vertical_order))
        self.form.mapper.toLast()
        self.form.show()

    def on_remove_clicked(self):
        if self.view.selectedIndexes():
            self.model.removeRow(self.view.selectedIndexes()[0].row())
            self.model.select()

    def on_move_up_clicked(self):
        current_index = self.view.currentIndex()
        if current_index != -1:
            self._move_up_or_down(current_index, MoveDirectionEnum.up)
            self.view.setCurrentIndex(
                current_index.sibling(current_index.row() - 1, current_index.column())
                if current_index.row() != 0
                else current_index
            )

    def on_move_down_clicked(self):
        current_index = self.view.currentIndex()
        if current_index != -1:
            self._move_up_or_down(current_index, MoveDirectionEnum.down)
            self.view.setCurrentIndex(
                current_index.sibling(current_index.row() + 1, current_index.column())
                if current_index.row() != current_index.model().rowCount() - 1
                else current_index
            )

    def _move_up_or_down(self, current_index, direction):
        old_vertical_order = current_index.sibling(current_index.row(), 1).data()
        new_vertical_order = old_vertical_order + direction.value
        row_to_swap = current_index.row() + direction.value
        self.model.setData(current_index.sibling(current_index.row(), 1), new_vertical_order)
        self.model.submitAll()
        self.model.setData(current_index.sibling(row_to_swap, 1), old_vertical_order)
        self.model.submitAll()
        self.model.lastError().text()
        self.model.select()

