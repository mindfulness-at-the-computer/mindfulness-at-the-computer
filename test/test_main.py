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
import mc.gui.warning_dlg


test_app = QtWidgets.QApplication(sys.argv)
# -has to be set here (rather than in __main__) to avoid an error


class MainTest(unittest.TestCase):
    """
    "@unittest.skip" can be used to skip a test
    """

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

    def test_breathing_dialog(self):
        mc.mc_global.active_phrase_id_it = 1
        breathing_dialog = mc.gui.breathing_dlg.BreathingDlg()

    def test_reminder_settings_dock(self):
        breathing_reminder_settings = mc.gui.breathing_settings_wt.BreathingSettingsWt()

    def test_breathing_history(self):
        breathing_history = mc.gui.breathing_history_wt.BreathingHistoryWt()

    def test_rest_action_list_dock(self):
        rest_action_list = mc.gui.rest_action_list_wt.RestActionListWt()

    def test_rest_reminder_settings_dock(self):
        rest_reminder_settings = mc.gui.rest_settings_wt.RestSettingsWt()

    def test_rest_dialog(self):
        rest_dialog = mc.gui.rest_dlg.RestDlg()

    def test_safe_delete_dialog(self):
        safe_delete_dialog = mc.gui.safe_delete_dlg.SafeDeleteDlg("testing")
        # self.assertTrue(safe_delete_dialog.show.isVisible())
        # self.assertTrue(safe_delete_dialog.description_qll.isVisibleTo(safe_delete_dialog))
        # self.assertTrue(safe_delete_dialog.isVisibleTo(None))
        ok_dialog_button = safe_delete_dialog.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QtTest.QTest.mouseClick(ok_dialog_button, QtCore.Qt.LeftButton)
        # self.assertFalse(safe_delete_dialog.isVisible())
        QtTest.QTest.waitForEvents()
        # self.assertFalse(safe_delete_dialog.description_qll.isVisibleTo(safe_delete_dialog))

    def test_add_dlg(self):
        add_dlg = mc.gui.warning_dlg.WarningDlg("testing")
        ok_dialog_button = add_dlg.button_box.button(QtWidgets.QDialogButtonBox.Ok)
        QtTest.QTest.mouseClick(ok_dialog_button, QtCore.Qt.LeftButton)
        QtTest.QTest.waitForEvents()

     def test_choose_music_button(self):
        choose_music = mc.gui.rest_dlg.RestDlg()
        if choose_music.choose_music_qpb.isEnabled():
            self.assertTrue(choose_music.on_choose_music_clicked)
        else:
            self.assertFalse(choose_music.on_choose_music_clicked)

    """
    def test_starting_breathing(self):
        main_win_widget = mc.gui.main_win.MbMainWindow()
        main_win_widget.menu_bar.
    """


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
