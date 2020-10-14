# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit, QListWidget

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


class MyListWidget(QListWidget, MyScrollableWidget): ...


class MyTextEdit(QPlainTextEdit, MyScrollableWidget):

    # 发送命令信号
    cmd_signal = pyqtSignal(str)
    
    def __init__(self, parent):
        super().__init__(parent)
        # 记录下是否获取到了返回值
        self.response = False

    def append_plain_text(self, text):
        """
        由于appendPlainText()方法默认会在末尾处添加新行，
        导致有的连续段落会终断，
        所以采用将光标移动到末尾然后插入新行方式
        """
        self.moveCursor(QTextCursor.End)
        self.insertPlainText(text)
        self.moveCursor(QTextCursor.End)
        self.setFocus()
        # 记录下输出文本的最后位置，作为用户输入的起始位置
        self.start_pos = self.textCursor().position()
        self.response = True

    def keyPressEvent(self, e):
        # 按下tab键，设置四个空格位
        if e.key() == Qt.Key_Tab:
            if self.response:
                text = self.get_text() + "\t"
                self.cmd_signal.emit(text)
                return
        elif e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            if self.response:
                text = self.get_text() + "\n"
                self.cmd_signal.emit(text)
        return super().keyPressEvent(e)

    def get_text(self):
        # 根据用户输入的结束位置，获取指定区间的文本
        self.end_pos = self.textCursor().position()
        cur = self.textCursor()
        cur.setPosition(self.start_pos, QTextCursor.MoveAnchor)
        # KeepAnchor 表示移动光标选中内容
        cur.setPosition(self.end_pos, QTextCursor.KeepAnchor)
        return cur.selectedText()

