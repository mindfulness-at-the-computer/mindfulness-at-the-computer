import sys
import unittest
from PyQt5 import QtTest
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.win.toggle_switch as ts

app = QtWidgets.QApplication(sys.argv)


class MainTest(unittest.TestCase):

    def test_first(self):
        assert 4 == 4

    def test_second(self):
        assert 5 == 5

    def test_third(self):
        ts_widget = ts.ToggleSwitchComposite()
        QtTest.QTest.mouseClick(ts_widget.on_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Enabled")
        QtTest.QTest.mouseClick(ts_widget.off_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Disabled")

if __name__ == "__main__":
    unittest.main()

