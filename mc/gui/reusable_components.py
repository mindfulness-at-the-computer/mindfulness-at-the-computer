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


class SunkenHorizontalLine(QtWidgets.QFrame):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Sunken)


class RaisedHorizontalLine(QtWidgets.QFrame):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Raised)
