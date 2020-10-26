# -*- coding: utf-8 -*-
from PyQt5.QtGui import QTextCharFormat, QFont, QBrush, QColor

_author_ = 'luwt'
_date_ = '2020/10/26 10:19'


class CharStyle:

    def __init__(self, code, fmt: QTextCharFormat):
        self.code = code
        self.fmt = fmt

    def set_style(self):
        # 加粗
        if self.code == 1:
            self.fmt.setFontWeight(QFont.Bold)
        # 减弱
        elif self.code == 2:
            pass
        # 斜体
        elif self.code == 3:
            self.fmt.setFontItalic(True)
        # 下划线
        elif self.code == 4:
            self.fmt.setFontUnderline(True)
        # 缓慢闪烁
        elif self.code == 5:
            pass
        # 快速闪烁
        elif self.code == 6:
            pass
        # 字体颜色反显
        elif self.code == 7:
            back = self.fmt.background().color()
            if back.name() == "#000000":
                self.fmt.setBackground(QBrush(QColor("white")))
            elif back.name() == "#FFFFFF":
                self.fmt.setBackground(QBrush(QColor("black")))
            self.fmt.setForeground(QBrush(back))
        # 隐藏，字体颜色设置为背景色即可
        elif self.code == 8:
            self.fmt.setForeground(QBrush(self.fmt.background().color()))
        # 删除线
        elif self.code == 9:
            self.fmt.setFontStrikeOut(True)


