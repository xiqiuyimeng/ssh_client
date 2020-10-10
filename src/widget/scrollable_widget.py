# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit

_author_ = 'luwt'
_date_ = '2020/10/10 10:25'


class MyScrollableWidget(QAbstractScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)

    def enterEvent(self, a0):
        """设置滚动条在进入控件区域的时候显示"""
        self.verticalScrollBar().setHidden(False)
        self.horizontalScrollBar().setHidden(False)

    def leaveEvent(self, a0):
        """设置滚动条在离开控件区域的时候隐藏"""
        self.verticalScrollBar().setHidden(True)
        self.horizontalScrollBar().setHidden(True)


class MyTextEdit(QPlainTextEdit, MyScrollableWidget):
    
    def __init__(self, parent):
        super().__init__(parent)
    #
    # def keyPressEvent(self, e):
    #     # 按下tab键，设置四个空格位
    #     if e.key() == Qt.Key_Tab:
    #         tc = self.textCursor()
    #         tc.insertText("    ")
    #         return
    #     return super().keyPressEvent(e)
