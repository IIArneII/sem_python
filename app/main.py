import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QColorDialog
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QPixmap
from ui.app_ui import Ui_MainWindow
from fieldWidget import FieldWidget
from date_dialog import DateDialog
from select_dialog import DialogId
from label_drop import LabelDrop
from db import DataBase
import copy
import re
import os.path


SETTINGS = 'settings/'


class App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.db = DataBase('http://localhost:3000/')
        self.mode = 'coll'
        self.rgb = None
        self.img_path = None
        self.param = None
        self.img = LabelDrop(self)
        self.fields = FieldWidget(self)
        self.setupUi(self)
        self.init_ui()

    def init_ui(self):
        self.layout_filters.addWidget(self.fields)
        self.set_collection_list()
        self.setup_settings()
        self.setStyleSheet(f'background:rgb({self.rgb});')
        if os.path.exists(self.img_path):
            self.img.setPixmap(self.img_path)
        else:
            self.img.setPixmap('logo.jpg')
        self.layout_img_filters.addWidget(self.img)
        self.collection_changed()
        self.box_coll.currentTextChanged.connect(self.collection_changed)
        self.box_param.currentTextChanged.connect(self.param_changed)
        self.coll_mode()
        self.btn_open.clicked.connect(self.open_selected)
        self.btn_find.clicked.connect(self.find)
        self.btn_del.clicked.connect(self.delete)
        self.btn_save.clicked.connect(self.save)
        self.btn_add.clicked.connect(self.add)
        self.btn_back.clicked.connect(self.collection_changed)
        self.btn_select.clicked.connect(self.select)
        self.table.itemDoubleClicked.connect(self.item_double_clicked)
        self.table.itemClicked.connect(self.item_clicked)
        self.table.itemChanged.connect(self.item_changed)
        self.color.triggered.connect(self.color_changed)

    def update_fields(self, fields: dict, fill: bool = False):
        # Обновляет виджеты с фильтрами или полями документа
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
        # обновляет таблицу и загружает в нее данные
        self.table.setCurrentCell(-1, 0)
        if not data and self.mode == 'doc':
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            if self.box_coll.currentText() == 'Shelfs':
                self.table.setColumnCount(2)
                self.table.setHorizontalHeaderLabels(['_id', 'name'])
            if self.box_coll.currentText() == 'Racks':
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(['_id'])
            if self.box_coll.currentText() == 'Storages':
                self.table.setColumnCount(1)
                self.table.setHorizontalHeaderLabels(['_id'])
            if self.box_coll.currentText() == 'ReadingRooms':
                if self.box_param.currentText() == 'librarians':
                    self.table.setColumnCount(3)
                    self.table.setHorizontalHeaderLabels(['_id', 'first_name', 'last_name'])
                if self.box_param.currentText() == 'items':
                    self.table.setColumnCount(2)
                    self.table.setHorizontalHeaderLabels(['_id', 'item_number'])
            if self.box_coll.currentText() == 'Libraries':
                if self.box_param.currentText() == 'cards':
                    self.table.setColumnCount(3)
                    self.table.setHorizontalHeaderLabels(['_id', 'first_name', 'last_name'])
                if self.box_param.currentText() == 'reading_rooms' or self.box_param.currentText() == 'storages':
                    self.table.setColumnCount(1)
                    self.table.setHorizontalHeaderLabels(['_id'])
            if self.box_coll.currentText() == 'Publications':
                if self.box_param.currentText() == 'attributes':
                    self.table.setColumnCount(2)
                    self.table.setHorizontalHeaderLabels(['v', 'k'])
                if self.box_param.currentText() == 'items':
                    self.table.setColumnCount(2)
                    self.table.setHorizontalHeaderLabels(['_id', 'item_number'])
                if self.box_param.currentText() == 'authors':
                    self.table.setColumnCount(3)
                    self.table.setHorizontalHeaderLabels(['_id', 'first_name', 'last_name'])
            if self.box_coll.currentText() == 'LibraryCards':
                if self.box_param.currentText() == 'rows':
                    self.table.setColumnCount(5)
                    self.table.setHorizontalHeaderLabels(
                        ['librarian', 'item', 'publication', 'issue_date', 'deadline_date', 'return_date'])
                if self.box_param.currentText() == 'attributes':
                    self.table.setColumnCount(2)
                    self.table.setHorizontalHeaderLabels(['v', 'k'])
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

    def open_selected(self):
        # Запрашивает у сервера данные по выбранному документу, обновляет поля и таблицу по полученным данным
        self.param = None
        self.box_param.clear()
        if self.box_coll.currentText() == 'Publications':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.publication_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['items'][0]:
                del param['items'][0]
            if not param['authors'][0]:
                del param['authors'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'Racks':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.racks_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['shelfs'][0]:
                del param['shelfs'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'Storages':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.storages_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['racks'][0]:
                del param['racks'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'Shelfs':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.shelfs_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['items'][0]:
                del param['items'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'ReadingRooms':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.reading_rooms_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['items'][0]:
                del param['items'][0]
            if not param['librarians'][0]:
                del param['librarians'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'Libraries':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.libraries_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['storages'][0]:
                del param['storages'][0]
            if not param['reading_rooms'][0]:
                del param['reading_rooms'][0]
            if not param['cards'][0]:
                del param['cards'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()
        if self.box_coll.currentText() == 'LibraryCards':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.library_cards_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            param = {i: data[i] for i in data if type(data[i]) == list}
            if not param['rows'][0]:
                del param['rows'][0]
            self.box_param.addItems(list(param.keys()))
            self.param = param
            # self.param_changed()

        if self.box_coll.currentText() == 'FundItems':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.fund_items_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            self.table.setCurrentCell(-1, 0)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
        if self.box_coll.currentText() == 'Librarians':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.librarians_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            self.table.setCurrentCell(-1, 0)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
        if self.box_coll.currentText() == 'Authors':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.authors_doc(match={'_id': id})[0]
            self.update_fields(data, fill=True)
            self.table.setCurrentCell(-1, 0)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
        self.doc_mode()
        self.param_changed()

    def find(self):
        # Поиск документов по выбранным фильтрам
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
        self.btn_del.setEnabled(False)
        self.btn_open.setEnabled(False)
        self.update_table(data)

    def delete(self):
        # Посылает на сервер команду удалить выбранный документ из БД
        if self.mode == 'coll':
            id = self.table.item(self.table.currentRow(), 0).text()
            data = self.db.delete(self.box_coll.currentText(), match={'_id': id})
            if data:
                self.table.removeRow(self.table.currentRow())
                self.btn_del.setEnabled(False)
                self.btn_open.setEnabled(False)
        elif self.mode == 'doc':
            del self.param[self.box_param.currentText()][self.table.currentRow()]
            self.table.removeRow(self.table.currentRow())

    def save(self):
        # обновляет документ из данных с полей и таблицы
        fields = self.fields.get_values(True)
        param = copy.deepcopy(self.param)
        if self.box_param.count() > 0:
            if self.box_coll.currentText() == 'LibraryCards' or self.box_coll.currentText() == 'Publications':
                for i in param:
                    if i == 'attributes':
                        atr = {i['k']: i['v'] for i in param[i]}
                        param[i] = atr
                    if i == 'rows':
                        for j in range(len(param[i])):
                            del param[i][j]['publication']
            if self.box_coll.currentText() == 'Publications' \
                    or self.box_coll.currentText() == 'Shelfs' \
                    or self.box_coll.currentText() == 'ReadingRooms' \
                    or self.box_coll.currentText() == 'Racks' \
                    or self.box_coll.currentText() == 'Storages' \
                    or self.box_coll.currentText() == 'Libraries':
                for i in param:
                    if i == 'authors' or i == 'items' or i == 'librarians' or i == 'shelfs' or i == 'racks' \
                            or i == 'storages' or i == 'reading_rooms' or i == 'cards':
                        val = [j['_id'] for j in param[i]]
                        param[i] = val
        if param:
            fields.update(param)
        data = self.db.post(self.box_coll.currentText(), fields)

    def select(self):
        # при редактировании ячейки таблицы в документе открывает диалоговые окна, где можно выбрать докумен или дату
        item = self.table.currentItem()
        key = self.table.horizontalHeaderItem(item.column()).text()
        if re.search('date', key):
            date = DateDialog.get_date()
            if date[0] == 'ok':
                if date[1] != '01.01.2000':
                    item.setText(date[1])
                else:
                    item.setText('')
        if (self.box_coll.currentText() == 'LibraryCards' and (key == 'item' or key == 'librarian')) or key == '_id':
            id = DialogId.get_id()
            if id[0] == 'ok':
                if id[1]:
                    item.setText(id[1])
                else:
                    item.setText('')

    def add(self):
        # Дабавляет строки в таблицу
        if self.mode == 'coll':
            data = self.db.put(self.box_coll.currentText())
            self.collection_changed()
        if self.mode == 'doc':
            self.table.setRowCount(self.table.rowCount() + 1)
            new = {}
            for i in range(self.table.columnCount()):
                new[self.table.horizontalHeaderItem(i).text()] = ''
            self.param[self.box_param.currentText()].append(new)

    def collection_changed(self):
        # При смене коллекции пользователем запрашивает документы из нее с сервера и обновляет таблицу и поля
        self.coll_mode()
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

    def param_changed(self):
        # При смене вложенного документа обновляет таблицу на данные из этого докумета
        self.btn_select.setEnabled(False)
        if self.param:
            self.update_table(self.param[self.box_param.currentText()])

    def coll_mode(self):
        # Переключает режим на режим коллекций - отображаются все документы из выбранной коллекции и фильтры
        self.mode = 'coll'
        self.lbl_filters.setText('Коллекция')
        self.table.setCurrentCell(-1, 0)

        self.btn_find.setHidden(False)
        self.btn_open.setHidden(False)
        self.btn_del.setHidden(False)

        self.btn_find.setEnabled(True)
        self.btn_open.setEnabled(False)
        self.btn_del.setEnabled(False)
        self.btn_add.setEnabled(True)

        self.btn_select.setHidden(True)
        self.btn_save.setHidden(True)
        self.btn_back.setHidden(True)
        self.box_param.setHidden(True)

    def doc_mode(self):
        # Переключает режим на режим документа - отображаются данные выбранного документа
        self.mode = 'doc'
        self.lbl_filters.setText('Документ')
        self.table.setCurrentCell(-1, 0)

        self.btn_find.setHidden(True)
        self.btn_open.setHidden(True)

        self.btn_select.setHidden(False)
        self.btn_save.setHidden(False)
        self.btn_back.setHidden(False)
        self.box_param.setHidden(False)

        self.btn_select.setEnabled(False)
        self.btn_del.setEnabled(False)
        self.btn_save.setEnabled(True)
        self.btn_back.setEnabled(True)

        if self.box_param.count() == 0:
            self.btn_add.setEnabled(False)
            self.btn_del.setEnabled(False)

    def item_clicked(self, item: QTableWidgetItem):
        # Срабатывает при нажатии на ячейку и делает активными некоторые кнопки
        if self.mode == 'coll':
            self.btn_del.setEnabled(True)
            self.btn_open.setEnabled(True)
        if self.mode == 'doc':
            self.btn_select.setEnabled(True)
            self.btn_del.setEnabled(True)

    def item_double_clicked(self, item: QTableWidgetItem):
        # При двойном нажатии на ячейку открывает выбранный документ,
        # либо вызывает всплывающее окно, если активен режим документа
        if self.mode == 'coll':
            self.open_selected()
        else:
            self.select()

    def item_changed(self, item: QTableWidgetItem):
        # Если ячейка таблицы меняется, то информация по ней сохраняется во вложенные документы выбранного документа
        if self.mode == 'doc':
            key = self.table.horizontalHeaderItem(item.column()).text()
            self.param[self.box_param.currentText()][item.row()][key] = item.text()

    def set_collection_list(self):
        # Запрашивает с сервера список всех коллекций и устанавливает их в выпадающий список
        data = self.db.collection_list()
        self.box_coll.addItems(data)

    def setup_settings(self):
        # Загружает сохраненные настройки из ini файла
        settings = QSettings("settings.ini", QSettings.IniFormat)
        coll = settings.value(SETTINGS + 'coll', 'LibraryCards', type=str)
        self.box_coll.setCurrentText(coll)
        x = settings.value(SETTINGS + 'x', 100, type=int)
        y = settings.value(SETTINGS + 'y', 100, type=int)
        self.move(x, y)
        width = settings.value(SETTINGS + 'width', 100, type=int)
        height = settings.value(SETTINGS + 'height', 100, type=int)
        self.resize(width, height)
        self.rgb = settings.value(SETTINGS + 'color', '255, 255, 255', type=str)
        self.img_path = settings.value(SETTINGS + 'img', 'logo.jpg', type=str)
        settings.sync()

    def save_settings(self):
        # Сохраняет настройки приложения в ini файл
        settings = QSettings("settings.ini", QSettings.IniFormat)
        settings.setValue(SETTINGS + 'coll', self.box_coll.currentText())
        settings.setValue(SETTINGS + 'x', self.x())
        settings.setValue(SETTINGS + 'y', self.y())
        settings.setValue(SETTINGS + 'width', self.width())
        settings.setValue(SETTINGS + 'height', self.height())
        settings.setValue(SETTINGS + 'color', self.rgb)
        print(self.img.url)
        settings.setValue(SETTINGS + 'img', self.img.url)
        settings.sync()

    def color_changed(self):
        color = QColorDialog.getColor()
        if color.value() != 0:
            rgb = color.getRgb()
            self.rgb = f'{rgb[0]}, {rgb[1]}, {rgb[2]}'
            self.setStyleSheet(f'background:rgb({self.rgb});')

    def closeEvent(self, e):
        # Вызывает при закрытии приложения метод сохранения настроек
        self.save_settings()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
