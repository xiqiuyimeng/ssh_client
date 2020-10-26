# -*- coding: utf-8 -*-
import re

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit, QListWidget

from src.widget.text_char_format.text_char_color import Color
from src.widget.text_char_format.text_char_style import CharStyle

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
        self.default_fmt = self.textCursor().charFormat()
        # 样式代码
        self.style_code = list(range(10))
        # 字体颜色代码
        self.font_color_code = list(range(30, 38)) + list(range(90, 98))
        # 背景色代码
        self.background_color_code = list(range(40, 48)) + list(range(100, 108))

    def append_plain_text(self, text):
        """
        由于appendPlainText()方法默认会在末尾处添加新行，
        导致有的连续段落会终断，
        所以采用将光标移动到末尾然后插入新行方式
        """
        self.moveCursor(QTextCursor.End)
        cursor = self.textCursor()
        pattern = re.compile(r'(\x1b\[0m)?\x1b\[(?P<fore>(\d{,3};)+)?(?P<back>\d{,3}m)(?P<text>.+?)\x1b\[0m')
        result = pattern.finditer(text)
        start = 0
        for r in result:
            fmt = QTextCharFormat()
            normal_text = text[start: r.span()[0]]
            # 先插入正常格式的文本
            cursor.insertText(normal_text)
            self.moveCursor(QTextCursor.End)
            # 处理文本样式
            if r.groupdict().get('fore'):
                fores = r.group('fore')[: -1].split(";")
                [self.set_format(int(fore), fmt) for fore in fores]
            if r.groupdict().get('back'):
                back = int(r.group('back')[: -1])
                self.set_format(back, fmt)
            color_text = r.group('text')
            cursor.setCharFormat(fmt)
            cursor.insertText(color_text)
            self.moveCursor(QTextCursor.End)
            cursor.setCharFormat(self.default_fmt)
            # 当前结尾作为下一个开始
            start = r.span()[1]
        rest_normal_text = text[start:]
        cursor.insertText(rest_normal_text)
        self.moveCursor(QTextCursor.End)
        self.setFocus()
        # 记录下输出文本的最后位置，作为用户输入的起始位置
        self.start_pos = self.textCursor().position()
        self.response = True

    def set_format(self, code, fmt):
        if code in self.style_code:
            CharStyle(code, fmt).set_style()
        elif code in self.font_color_code:
            Color(code, fmt).set_foreground_color()
        elif code in self.background_color_code:
            Color(code, fmt).set_background_color()

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

