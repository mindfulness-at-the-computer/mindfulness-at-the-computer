from PyQt5 import QtWidgets


class H1(QtWidgets.QLabel):
    """
    Heading 1
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class H2(QtWidgets.QLabel):
    """
    Heading 2
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class HorizontalLine(QtWidgets.QFrame):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFrameShape(self.HLine)


class RadioButtonLeft(QtWidgets.QRadioButton):
    """
    The left button of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class RadioButtonMiddle(QtWidgets.QRadioButton):
    """
    One of the middle buttons of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class RadioButtonRight(QtWidgets.QRadioButton):
    """
    The right button of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)


class PushButton(QtWidgets.QPushButton):
    """
    The left button of a radio button group
    """
    def __init__(self, *__args):
        super().__init__(*__args)
