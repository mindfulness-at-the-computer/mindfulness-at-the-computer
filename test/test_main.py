import sys
import unittest
from PyQt5 import QtTest
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

import mc.gui.toggle_switch_cw as ts
import mc.gui.phrase_list_cw as pl
import mc.mc_global

app = QtWidgets.QApplication(sys.argv)
# -has to be set here (rather than in __main__) to avoid an error

# TODO: find a way to set the testing flag or other way to run in memory instead of on disk
# for the database as well as for the other files
# PLEASE NOTE: We are not going to create new or write to files except for the database file


class MainTest(unittest.TestCase):

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
        QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb, QtCore.Qt.LeftButton)

        text_list = []
        for i in range(0, pl_widget.list_widget.count()):
            qlwi = pl_widget.list_widget.item(i)
            custom_qll = pl_widget.list_widget.itemWidget(qlwi)
            #text_list.append(custom_qll.text())
            if custom_qll.text() == TEST_TEXT_STR:
                return
        #self.assertIn(TEST_TEXT_STR, text_list)
        self.fail()

    def test_selecting_breathing_phrase(self):
        self.assertTrue(True)


if __name__ == "__main__":
    mc.mc_global.testing_bool = True
    unittest.main()

