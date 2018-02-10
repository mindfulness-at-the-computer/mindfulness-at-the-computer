import sys
import unittest
from PyQt5 import QtTest
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.mc_global
import mc.gui.toggle_switch_wt
import mc.gui.breathing_dlg
import mc.gui.breathing_phrase_list_wt
import mc.gui.breathing_settings_wt
import mc.gui.breathing_history_wt
import mc.gui.main_win
import mc.gui.rest_action_list_wt
import mc.gui.rest_settings_wt
import mc.gui.rest_dlg
import mc.gui.safe_delete_dlg
import mc.gui.toggle_switch_wt


class MainTest(unittest.TestCase):
    """
    "@unittest.skip" can be used to skip a test
    """

    @classmethod
    def setUpClass(cls):
        mc.mc_global.testing_bool = True

    def setUp(self):
        pass

    def test_create(self):
        breathing_phrase_list = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()

    def test_add_phrase(self):
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()

        TEST_TEXT_STR = "testing 1"
        QtTest.QTest.keyClicks(pl_widget.add_to_list_qle, TEST_TEXT_STR)
        QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb, QtCore.Qt.LeftButton)

        pl_widget.edit_dialog.accept()  # clicking "ok"
        # pl_widget.edit_dialog.reject()

        # QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb, QtCore.Qt.LeftButton)

        # trying to find the newly added entry
        for i in range(0, pl_widget.list_widget.count()):
            qlwi = pl_widget.list_widget.item(i)
            custom_qll = pl_widget.list_widget.itemWidget(qlwi)
            if custom_qll.text() == TEST_TEXT_STR:
                return
        else:
            self.fail()

    def test_delete_single(self):
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        list_length_before_int = pl_widget.list_widget.count()
        pl_widget.list_widget.takeItem(0)
        self.assertEqual(list_length_before_int - 1, pl_widget.list_widget.count())

    def test_delete_two(self):
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        list_length_before_int = pl_widget.list_widget.count()
        pl_widget.list_widget.takeItem(0)
        pl_widget.list_widget.takeItem(0)
        self.assertEqual(list_length_before_int - 2, pl_widget.list_widget.count())

    def test_delete_all(self):
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        while pl_widget.list_widget.takeItem(0):
            pass
        self.assertEqual(pl_widget.list_widget.count(), 0)

