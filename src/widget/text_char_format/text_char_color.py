# -*- coding: utf-8 -*-
from PyQt5.QtGui import QTextCharFormat, QBrush, QColor

_author_ = 'luwt'
_date_ = '2020/10/26 14:35'


color_dict = {
    # 黑色
    30: (0, 0, 0),
    # 红色
    31: (204, 0, 0),
    # 绿色
    32: (78, 154, 6),
    # 黄色
    33: (196, 160, 0),
    # 蓝色
    34: (52, 101, 164),
    # 洋红色
    35: (117, 80, 123),
    # 青色
    36: (6, 152, 154),
    # 白色
    37: (211, 215, 207),
    # 亮黑色
    90: (85, 87, 83),
    # 亮红色
    91: (239, 41, 41),
    # 亮绿色
    92: (138, 226, 52),
    # 亮黄色
    93: (252, 233, 79),
    # 亮蓝色
    94: (114, 159, 207),
    # 亮洋红色
    95: (173, 127, 168),
    # 亮青色
    96: (52, 226, 226),
    # 亮白色
    97: (238, 238, 236)
}


class Color:

    def __init__(self, code, fmt: QTextCharFormat):
        self.code = code
        self.fmt = fmt

    def set_foreground_color(self):
        self.fmt.setForeground(QBrush(QColor(*color_dict.get(self.code))))

    def set_background_color(self):
        self.fmt.setBackground(QBrush(QColor(*color_dict.get(self.code - 10))))
