from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QDropEvent, QDragEnterEvent, QDragMoveEvent, QPixmap


class LabelDrop(QLabel):
    def __init__(self, parent):
        super(LabelDrop, self).__init__(parent)
        self.url = None
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e: QDragEnterEvent) -> None:
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e: QDragMoveEvent) -> None:
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e: QDropEvent) -> None:
        if e.mimeData().text()[0: 8] == 'file:///' and \
                (e.mimeData().text()[-1: -5: -1][::-1] == '.png' or e.mimeData().text()[-1: -5: -1][::-1] == '.jpg'):
            self.url = e.mimeData().text()[8:]
            super(LabelDrop, self).setPixmap(QPixmap(self.url))
        else:
            super(LabelDrop, self).setPixmap(QPixmap('logo.jpg'))

    def setPixmap(self, path):
        self.url = path
        super(LabelDrop, self).setPixmap(QPixmap(path))
