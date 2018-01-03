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


test_app = QtWidgets.QApplication(sys.argv)
# -has to be set here (rather than in __main__) to avoid an error


class MainTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mc.mc_global.testing_bool = True

    def setUp(self):
        pass

    def test_toggle_switch(self):
        ts_widget = mc.gui.toggle_switch_wt.ToggleSwitchWt()

        QtTest.QTest.mouseClick(ts_widget.off_qpb, QtCore.Qt.LeftButton)

        QtTest.QTest.mouseClick(ts_widget.on_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Enabled")
        self.assertTrue(ts_widget.on_qpb.isChecked())
        self.assertFalse(ts_widget.off_qpb.isChecked())

        QtTest.QTest.mouseClick(ts_widget.off_qpb, QtCore.Qt.LeftButton)
        self.assertEqual(ts_widget.state_qll.text(), "Disabled")
        self.assertFalse(ts_widget.on_qpb.isChecked())
        self.assertTrue(ts_widget.off_qpb.isChecked())

    def test_main_window(self):
        main_window = mc.gui.main_win.MainWin()

    @unittest.skip
    def test_breathing_dialog(self):
        breathing_dialog = mc.gui.breathing_dlg.BreathingDlg()

    def test_breathing_phrase_list_dock(self):
        breathing_phrase_list_dock = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()

    def test_reminder_settings_dock(self):
        breathing_reminder_settings_dock = mc.gui.breathing_settings_wt.BreathingSettingsWt()

    def test_breathing_widget(self):
        breathing_widget = mc.gui.breathing_history_wt.BreathingHistoryWt()

    def test_rest_action_list_dock(self):
        rest_action_list_dock = mc.gui.rest_action_list_wt.RestActionListWt()

    def test_rest_reminder_settings_dock(self):
        rest_reminder_settings_dock = mc.gui.rest_settings_wt.RestSettingsWt()

    def test_rest_widget(self):
        rest_widget = mc.gui.rest_dlg.RestDlg()

    def test_safe_delete_dialog(self):
        safe_delete_dialog = mc.gui.safe_delete_dlg.SafeDeleteDlg("testing")
        ok_dialog_button = safe_delete_dialog.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QtTest.QTest.mouseClick(ok_dialog_button, QtCore.Qt.LeftButton)

    @unittest.skip
    def test_adding_breathing_phrase(self):
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()

        TEST_TEXT_STR = "testing 1"
        QtTest.QTest.keyClicks(pl_widget.add_to_list_qle, TEST_TEXT_STR)
        QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb, QtCore.Qt.LeftButton)

        for i in range(0, pl_widget.list_widget.count()):
            qlwi = pl_widget.list_widget.item(i)
            custom_qll = pl_widget.list_widget.itemWidget(qlwi)
            if custom_qll.text() == TEST_TEXT_STR:
                return
        self.fail()

    """
    def test_starting_breathing(self):
        main_win_widget = mc.gui.main_win.MbMainWindow()
        main_win_widget.menu_bar.
    """

    def est_selecting_breathing_phrase(self):

        # pl_widget = self.matc_main_obj.main_window.phrase_list_widget
        pl_widget = mc.gui.breathing_phrase_list_wt.BreathingPhraseListWt()
        # breathing_widget = self.matc_main_obj.main_window.breathing_composite_widget
        breathing_widget = mc.gui.breathing_history_wt.BreathingHistoryWt()
        print("breathing_widget.bi_text_qll.text() = " + breathing_widget.bi_text_qll.text())

        # mc.gui.main_win.MbMainWindow()

        TEXT_FOR_ENTRY_TO_CLICK_STR = "testing 2"
        QtTest.QTest.keyClicks(pl_widget.add_to_list_qle, TEXT_FOR_ENTRY_TO_CLICK_STR)
        QtTest.QTest.mouseClick(pl_widget.add_new_phrase_qpb, QtCore.Qt.LeftButton)

        # pl_widget.list_widget.setCurrentRow(3)

        for i in range(0, pl_widget.list_widget.count()):
            qlwi = pl_widget.list_widget.item(i)
            custom_qll = pl_widget.list_widget.itemWidget(qlwi)
            if custom_qll.text() == TEXT_FOR_ENTRY_TO_CLICK_STR:
                # pl_widget.list_widget.setCurrentItem(qlwi)
                qlwi_rect = pl_widget.list_widget.visualItemRect(qlwi)
                QtTest.QTest.mouseClick(
                    pl_widget.list_widget.viewport(),
                    QtCore.Qt.LeftButton,
                    pos=qlwi_rect.center()
                )

        QtTest.QTest.waitForEvents()

        print("breathing_widget.bi_text_qll.text() = " + breathing_widget.bi_text_qll.text())
        print("mc.gui.phrase_list_cw.BREATHING_IN_DEFAULT_PHRASE = "
              + mc.gui.breathing_phrase_list_wt.BREATHING_IN_DEFAULT_PHRASE)
        is_true = breathing_widget.bi_text_qll.text() == mc.gui.breathing_phrase_list_wt.BREATHING_IN_DEFAULT_PHRASE

        self.assertTrue(is_true)

        self.assertTrue(
            breathing_widget.bo_text_qll.text() == mc.gui.breathing_phrase_list_wt.BREATHING_OUT_DEFAULT_PHRASE
        )

    @staticmethod
    def click_on_list_widget_entry(
            i_list_widget: QtWidgets.QListWidget,
            i_text_for_entry_to_click: str):
        # -this assumes that the list widget has a custom qlwi set for each of the rows
        for i in range(0, i_list_widget.count()):
            qlwi = i_list_widget.item(i)
            custom_qll = i_list_widget.itemWidget(qlwi)
            if custom_qll.text() == i_text_for_entry_to_click:
                QtTest.QTest.mouseClick(custom_qll, QtCore.Qt.LeftButton)
                return True
        return False


if __name__ == "__main__":
    unittest.main()


"""
def __init__(self, *args, **kwargs):
    super(MainTest, self).__init__(*args, **kwargs)
    # -https://stackoverflow.com/questions/17353213/init-for-unittest-testcase
    
pl_widget.list_widget.itemWidget()

Things to test:
*


        QtCore.QCoreApplication.processEvents()
        QtTest.QTest.waitForEvents()  # <-------------------
        QtTest.QTest.qWait(3000)
        res_bl = self.click_on_list_widget_entry(pl_widget.list_widget, TEXT_FOR_ENTRY_TO_CLICK_STR)
        if not res_bl:
            self.fail()

    def test_take_a_break_now(self):
        take_break_qpb = self.matc_main_obj.main_window.rest_settings_widget.rest_reminder_test_qpb
        rr_dlg = self.matc_main_obj.main_window.rest_reminder_dialog
        QtTest.QTest.mouseClick(take_break_qpb, QtCore.Qt.LeftButton)
        QtTest.QTest.mouseClick(rr_dlg.close_qpb, QtCore.Qt.LeftButton)

 
"""

# TODO: Make sure that this is the first time the application has been started
