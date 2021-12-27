from ui.date_dialog_ui import Ui_Dialog
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog


class DateDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super(DateDialog, self).__init__()
        self.mode = 'close'
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.btn_ok.clicked.connect(self.btn_clicked)
        self.btn_close.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        if self.sender() == self.btn_close:
            self.close()
        if self.sender() == self.btn_ok:
            self.mode = 'ok'
            self.close()

    @staticmethod
    def get_date(date: str = ''):
        dialog = DateDialog()
        if date:
            d = list(map(int, date.split('.')))
            dialog.line_date.setDate(QDate(d[2], d[1], d[0]))
        dialog.exec_()
        return dialog.mode, dialog.line_date.date().toString('dd.MM.yyyy')
