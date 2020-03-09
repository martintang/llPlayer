from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import QWidget


class MaskWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint, True)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet('background:rgba(0,0,0,255);')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMouseTracking(True)
        self.ratio = 13 / 15
        self.top_drag = False
        self.top_rect = []
        self.parent_rect = None

    def mouseMoveEvent(self, a0: QMouseEvent):
        # 判断鼠标位置切换鼠标手势
        if a0.pos() in self.top_rect:
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        if Qt.LeftButton and self.top_drag:
            # 调整窗口高度
            top = self.parent_rect.height() * self.ratio + a0.pos().y()
            self.ratio = top / self.parent_rect.height()
            self.setGeometry(self.parent_rect)
            a0.accept()

    def mousePressEvent(self, a0: QMouseEvent):
        if (a0.button() == Qt.LeftButton) and (a0.pos() in self.top_rect):
            # 鼠标左键点击右下角边界区域
            self.top_drag = True
            a0.accept()

    def mouseReleaseEvent(self, a0: QMouseEvent):
        self.top_drag = False
        super().mouseReleaseEvent(a0)

    def resizeEvent(self, a0: QResizeEvent):
        self.top_rect = [QPoint(x, y) for x in range(5, self.width() - 5)
                         for y in range(-5, 5)]

    def setGeometry(self, a0: QtCore.QRect):
        self.parent_rect = QtCore.QRect(a0)
        a0.setLeft(0)
        a0.setTop(a0.height() * self.ratio)
        super().setGeometry(a0)

    def show(self):
        if self.parent() is None:
            return

        self.setGeometry(self.parent().geometry())
        super().show()
