# -*- coding: utf-8 -*-
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QTextCharFormat, QBrush, QColor, QFont
from PyQt5.QtWidgets import QAbstractScrollArea, QPlainTextEdit, QListWidget
import re

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
        # 字体样式：1-9, 1 加粗 2 减弱 3 斜体 4 下划线 7 反转 8 隐藏 9 删除线
        # 前景色：30-37， 30黑 31红 32绿 33黄 34蓝 35品红 36青 37白
        # 明亮版前景色：90-97，90亮黑 91亮红 92亮绿 93亮黄 94亮蓝 95亮品红 96亮青 97亮白
        # 背景色：40-47，40黑 41红 42绿 43黄 44蓝 45品红 46青 47白
        # 明亮版背景色：100-107，100亮黑 101亮红 102亮绿 103亮黄 104亮蓝 105亮品红 106亮青 107亮白
        self.moveCursor(QTextCursor.End)
        cursor = self.textCursor()
        default_fmt = cursor.charFormat()
        pattern = re.compile(r'(\x1b\[0m)?\x1b\[(?P<fore>\d{,3};)?(?P<back>\d{,3}m)(?P<text>.+?)\x1b\[0m')
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
                fore = int(r.group('fore')[: -1])
                # 1-9为字体样式
                if 1 <= fore <= 9:
                    if fore == 1:
                        fmt.setFontWeight(QFont.Bold)
                elif 30 <= fore <= 37:
                    if fore == 34:
                        color = 114, 159, 207
                        fmt.setForeground(QBrush(QColor(*color)))
            back = r.group('back')[: -1]
            if int(back) == 34:
                color = 114, 159, 207
                fmt.setForeground(QBrush(QColor(*color)))
            color_text = r.group('text')
            cursor.setCharFormat(fmt)
            cursor.insertText(color_text)
            self.moveCursor(QTextCursor.End)
            cursor.setCharFormat(default_fmt)
            # 当前结尾作为下一个开始
            start = r.span()[1]
        rest_normal_text = text[start:]
        cursor.insertText(rest_normal_text)
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

