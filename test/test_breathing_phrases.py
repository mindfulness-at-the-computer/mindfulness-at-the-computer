import sys
import os
import unittest
import random
from PyQt5 import QtTest
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import mc.mc_global
import mc.db
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


SEED_INT = 1


class BreathingPhrasesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mc.mc_global.testing_bool = True

    def setUp(self):
        random.seed(SEED_INT)  # making sure that the number will be pseudo-random
        self.bpl = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()

    def tearDown(self):
        mc.db.Helper.close_db()

    def test_create(self):
        pass

    def test_add_phrase_single(self):
        test_text_str = "testing 1"
        self.add_to_list(test_text_str)

    def test_add_phrase_multiple(self):
        base_test_text_str = "testing"
        number_to_add_int = 10
        for i in range(0, number_to_add_int):
            test_text_str = base_test_text_str + " " + str(i)
            self.add_to_list(test_text_str)

    def add_to_list(self, i_string: str):
        QtTest.QTest.keyClicks(self.bpl.add_to_list_qle, i_string)
        QtTest.QTest.mouseClick(self.bpl.add_new_phrase_qpb, QtCore.Qt.LeftButton)
        self.bpl.edit_dialog.accept()  # clicking "ok"
        self.assertTrue(self.is_in_list(self.bpl.list_widget, i_string))

    @staticmethod
    def is_in_list(i_list: list, i_string: str):
        for i in range(0, i_list.count()):
            qlwi = i_list.item(i)
            custom_qll = i_list.itemWidget(qlwi)
            if custom_qll.text() == i_string:
                return True
        return False

    def test_delete_single(self):
        list_length_before_int = self.bpl.list_widget.count()
        self.bpl.list_widget.takeItem(0)
        self.assertEqual(list_length_before_int - 1, self.bpl.list_widget.count())

    def test_delete_two(self):
        list_length_before_int = self.bpl.list_widget.count()
        self.bpl.list_widget.takeItem(0)
        self.bpl.list_widget.takeItem(0)
        self.assertEqual(list_length_before_int - 2, self.bpl.list_widget.count())

    def test_delete_all(self):
        while self.bpl.list_widget.takeItem(0):
            pass
        self.assertEqual(self.bpl.list_widget.count(), 0)

    def test_click_on_entry(self):
        test_nonexisting_text_str = "non-existing"
        test_text_str = "existing"
        self.add_to_list(test_text_str)
        self.assertFalse(self.click_on_list_widget_entry(test_nonexisting_text_str))
        self.bpl.list_widget.setCurrentRow(0)
        self.assertTrue(self.click_on_list_widget_entry(test_text_str))
        self.assertEqual(self.bpl.list_widget.currentRow(), self.bpl.list_widget.count() - 1)
        self.print_current_row_and_count("test_click_on_entry")

    def print_current_row_and_count(self, i_init_string: str):
        equals_signs_str = " ========= "
        print(equals_signs_str + i_init_string + equals_signs_str)
        print("self.bpl.list_widget.currentRow() = " + str(self.bpl.list_widget.currentRow()))
        print("self.bpl.list_widget.count() = " + str(self.bpl.list_widget.count()))
        print(equals_signs_str)

    def click_on_list_widget_entry(self, i_text_for_entry_to_click: str):
        # -this assumes that the list widget has a custom qlwi set for each of the rows
        for i in range(0, self.bpl.list_widget.count()):
            qlwi = self.bpl.list_widget.item(i)
            custom_qll = self.bpl.list_widget.itemWidget(qlwi)
            qlwi_qrect = self.bpl.list_widget.visualItemRect(qlwi)
            if custom_qll.text() == i_text_for_entry_to_click:
                # QtTest.QTest.mouseClick(qlwi, QtCore.Qt.LeftButton)
                QtTest.QTest.mouseClick(
                    self.bpl.list_widget.viewport(),
                    QtCore.Qt.LeftButton,
                    pos=qlwi_qrect.center()
                )
                QtTest.QTest.waitForEvents()
                return True
        return False

    """
    # This doesn't work
    def click_on_list_widget_entry(self, i_text_for_entry_to_click: str):
        # -this assumes that the list widget has a custom qlwi set for each of the rows
        for i in range(0, self.bpl.list_widget.count()):
            qlwi = self.bpl.list_widget.item(i)
            custom_qll = self.bpl.list_widget.itemWidget(qlwi)
            if custom_qll.text() == i_text_for_entry_to_click:
                QtTest.QTest.mouseClick(custom_qll, QtCore.Qt.LeftButton)
                return True
        return False
    """
