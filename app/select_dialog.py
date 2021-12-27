import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QDialog
from ui.select_dialog_ui import Ui_Dialog
from fieldWidget import FieldWidget
from db import DataBase


class DialogId(QDialog, Ui_Dialog):
    def __init__(self):
        super(DialogId, self).__init__()
        self.mode = 'close'
        self.id = None
        self.db = DataBase('http://localhost:3000/')
        self.fields = FieldWidget(self)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.layout_field.addWidget(self.fields)
        self.set_collection_list()
        self.collection_changed()
        self.box_coll.currentTextChanged.connect(self.collection_changed)
        self.btn_select.clicked.connect(self.select)
        self.btn_void.clicked.connect(self.void)
        self.btn_find.clicked.connect(self.find)
        self.table.itemDoubleClicked.connect(self.select)
        self.table.itemClicked.connect(self.item_clicked)

    def void(self):
        self.mode = 'ok'
        self.close()

    def select(self):
        self.mode = 'ok'
        self.id = self.table.item(self.table.currentRow(), 0).text()
        self.close()

    @staticmethod
    def get_id():
        dialog = DialogId()
        dialog.exec_()
        return dialog.mode, dialog.id

    def update_fields(self, fields: dict, fill: bool = False):
        self.fields.clear()
        for i in fields:
            typ = self.db.type_data(fields[i])
            if typ != 'dict' and typ != 'list':
                if fill:
                    if i != '_id':
                        self.fields.add_field(i, typ, False, fields[i])
                    else:
                        self.fields.add_field(i, typ, False, fields[i], enabled=False)
                else:
                    self.fields.add_field(i, typ, typ in ['date', 'num'])

    def update_table(self, data):
        self.table.setCurrentCell(-1, 0)
        if not data:
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return
        self.table.setColumnCount(len(data[0]))
        self.table.setHorizontalHeaderLabels(list(data[0].keys()))
        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(data[i][elem])))

        self.table.showColumn(0)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    def find(self):
        data = None
        if self.box_coll.currentText() == 'Publications':
            data = self.db.publication_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Racks':
            data = self.db.racks_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Storages':
            data = self.db.storages_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Shelfs':
            data = self.db.shelfs_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'FundItems':
            data = self.db.fund_items_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Librarians':
            data = self.db.librarians_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Authors':
            data = self.db.authors_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'ReadingRooms':
            data = self.db.reading_rooms_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'Libraries':
            data = self.db.libraries_list(match=self.fields.get_values())
        elif self.box_coll.currentText() == 'LibraryCards':
            data = self.db.library_cards_list(match=self.fields.get_values())
        self.update_table(data)

    def collection_changed(self):
        self.btn_select.setEnabled(False)
        data = None
        if self.box_coll.currentText() == 'Publications':
            data = self.db.publication_list()
        elif self.box_coll.currentText() == 'Racks':
            data = self.db.racks_list()
        elif self.box_coll.currentText() == 'Storages':
            data = self.db.storages_list()
        elif self.box_coll.currentText() == 'Shelfs':
            data = self.db.shelfs_list()
        elif self.box_coll.currentText() == 'FundItems':
            data = self.db.fund_items_list()
        elif self.box_coll.currentText() == 'Librarians':
            data = self.db.librarians_list()
        elif self.box_coll.currentText() == 'Authors':
            data = self.db.authors_list()
        elif self.box_coll.currentText() == 'ReadingRooms':
            data = self.db.reading_rooms_list()
        elif self.box_coll.currentText() == 'Libraries':
            data = self.db.libraries_list()
        elif self.box_coll.currentText() == 'LibraryCards':
            data = self.db.library_cards_list()
        self.update_table(data)
        self.update_fields(data[0])

    def item_clicked(self):
        self.btn_select.setEnabled(True)

    def set_collection_list(self):
        data = self.db.collection_list()
        self.box_coll.addItems(data)

