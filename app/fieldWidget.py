from PyQt5.QtWidgets import QWidget, QDateEdit, QSizePolicy, QSpinBox, QLabel, QLineEdit
from PyQt5.QtCore import QDate
from ui.field_ui import Ui_Form
import re


class FieldWidget(QWidget, Ui_Form):
    def __init__(self, parent):
        super(FieldWidget, self).__init__(parent)
        self.row = 0
        self.rows = []
        self.setupUi(self)

    def clear(self):
        # Удаляет все поля
        for i in self.rows:
            for j in i:
                self.gridLayout.removeWidget(j)
                j.deleteLater()
                j = None
        self.rows.clear()
        self.row = 0

    def get_values(self, all=False):
        # возращает значения всех полей
        if not all:
            values = {}
            for i in self.rows:
                if len(i) == 2:
                    if type(i[1]) == QLineEdit:
                        if i[1].text():
                            values[i[0].text() + '*r'] = i[1].text()
                    if type(i[1]) == QSpinBox:
                        if i[1].value() != 0:
                            values[i[0].text()] = i[1].value()
                    if type(i[1]) == QDateEdit:
                        d1 = i[1].date().toString('yyyy-MM-dd')
                        if d1 != '2000-01-01':
                            values[i[0].text()] = d1
                if len(i) == 4:
                    if type(i[1]) == QLineEdit:
                        if i[1].text() or i[3].text():
                            values[i[0].text() + '*b'] = [i[1].text(), i[3].text()]
                    if type(i[1]) == QSpinBox:
                        if i[1].value() != 0 or i[3].value() != 0:
                            values[i[0].text() + '*b'] = [i[1].value(), i[3].value()]
                    if type(i[1]) == QDateEdit:
                        d1 = i[1].date().toString('yyyy-MM-dd')
                        d2 = i[3].date().toString('yyyy-MM-dd')
                        if d1 != '2000-01-01' and d2 != '2000-01-01':
                            values[i[0].text() + '*b'] = [d1, d2]
            return values
        else:
            values = {}
            for i in self.rows:
                if type(i[1]) == QLineEdit:
                    if i[1].text():
                        values[i[0].text()] = i[1].text()
                    else:
                        values[i[0].text()] = None
                if type(i[1]) == QSpinBox:
                    if i[1].value() != 0:
                        values[i[0].text()] = i[1].value()
                    else:
                        values[i[0].text()] = None
                if type(i[1]) == QDateEdit:
                    d1 = i[1].date().toString('yyyy-MM-dd')
                    if d1 != '2000-01-01':
                        values[i[0].text()] = d1
                    else:
                        values[i[0].text()] = None
            return values

    def add_field(self, name: str, typ: str, between: bool = False, value=None, enabled: bool = True) -> None:
        # Добавляет новое поле
        self.rows.append([])

        lbl = QLabel(name, self)
        lbl.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.gridLayout.addWidget(lbl, self.row, 0, 1, 1)
        self.rows[-1].append(lbl)

        if typ == 'date' or re.search('date', name):
            line = QDateEdit(self)
            line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            line.setMinimumSize(300, 0)
            self.gridLayout.addWidget(line, self.row, 1, 1, 1)
            if value:
                d = list(map(int, value.split('.')))
                line.setDate(QDate(d[2], d[1], d[0]))
            else:
                line.setDate(QDate(0, 0, 0))
            if not enabled:
                line.setEnabled(False)
            self.rows[-1].append(line)

        elif typ == 'str':
            line = QLineEdit(value, self)
            line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            line.setMinimumSize(300, 0)
            if not enabled:
                line.setEnabled(False)
            self.gridLayout.addWidget(line, self.row, 1, 1, 1)
            self.rows[-1].append(line)
        elif typ == 'num':
            line = QSpinBox(self)
            line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
            line.setMinimumSize(300, 0)
            line.setMaximum(100000000)
            if value:
                line.setValue(value)
            if not enabled:
                line.setEnabled(False)
            self.gridLayout.addWidget(line, self.row, 1, 1, 1)
            self.rows[-1].append(line)

        if value == None and (between or re.search('date', name)):
            lbl = QLabel('-', self)
            lbl.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.gridLayout.addWidget(lbl, self.row, 2, 1, 1)
            self.rows[-1].append(lbl)

            if typ == 'date' or re.search('date', name):
                line = QDateEdit(self)
                line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                line.setMinimumSize(300, 0)
                self.gridLayout.addWidget(line, self.row, 3, 1, 1)
                if value:
                    d = list(map(int, value.split('.')))
                    line.setDate(QDate(d[2], d[1], d[0]))
                if not enabled:
                    line.setEnabled(False)
                self.rows[-1].append(line)
            elif typ == 'str':
                line = QLineEdit(value, self)
                line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                line.setMinimumSize(300, 0)
                self.gridLayout.addWidget(line, self.row, 3, 1, 1)
                self.rows[-1].append(line)
            elif typ == 'num':
                line = QSpinBox(self)
                line.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
                line.setMinimumSize(300, 0)
                line.setMaximum(100000000)
                if value:
                    line.setValue(value)
                if not enabled:
                    line.setEnabled(False)
                self.gridLayout.addWidget(line, self.row, 3, 1, 1)
                self.rows[-1].append(line)

        self.row += 1
