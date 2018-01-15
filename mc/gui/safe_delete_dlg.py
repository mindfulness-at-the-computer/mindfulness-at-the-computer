from PyQt5 import QtWidgets
from PyQt5 import QtCore


class SafeDeleteDlg(QtWidgets.QDialog):
    """
    Inspiration: Answer by lou here:
    https://stackoverflow.com/questions/18196799/how-can-i-show-a-pyqt-modal-dialog-and-get-data-out-of-its-controls-once-its-clo
    """
    def __init__(self, i_description_str: str, i_parent=None) -> None:
        super(SafeDeleteDlg, self).__init__(i_parent)

        vbox = QtWidgets.QVBoxLayout(self)

        self.description_qll = QtWidgets.QLabel(i_description_str)
        vbox.addWidget(self.description_qll)

        self.button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self
        )
        vbox.addWidget(self.button_box)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        # -accept and reject are "slots" built into Qt

    @staticmethod
    def get_safe_confirmation_dialog(i_description_str: str) -> bool:
        dialog = SafeDeleteDlg(i_description_str)
        dialog_result = dialog.exec_()
        confirmation_result_bool = False
        if dialog_result == QtWidgets.QDialog.Accepted:
            confirmation_result_bool = True
        return confirmation_result_bool
