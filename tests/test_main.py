import sys
import unittest
from PyQt5 import QtTest
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.win.toggle_switch as ts
import mc.win.phrase_list as pl

app = QtWidgets.QApplication(sys.argv)


class MainTest(unittest.TestCase):

    def test_first(self):
        assert 4 == 4

    def test_toggle_switch(self):
        ts_widget = ts.ToggleSwitchComposite()

        QtTest.QTest.mouseClick(ts_widget.off_qpb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(ts_widget.on_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Enabled")
        self.assertTrue(ts_widget.on_qpb.isChecked())
        self.assertFalse(ts_widget.off_qpb.isChecked())

        QtTest.QTest.mouseClick(ts_widget.off_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Disabled")
        self.assertFalse(ts_widget.on_qpb.isChecked())
        self.assertTrue(ts_widget.off_qpb.isChecked())

    def test_adding_breathing_phrase(self):
        pl_widget = pl.PhraseListCompositeWidget()

        TEST_TEXT_STR = "testing 1"
        QtTest.QTest.keyClicks(pl_widget.add_to_list_qle, TEST_TEXT_STR)
        QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb)

        for i in range(0, pl_widget.list_widget.count()):
            text_list = pl_widget.list_widget.item(i).text()
        self.assertIn(TEST_TEXT_STR, text_list)


if __name__ == "__main__":
    unittest.main()

