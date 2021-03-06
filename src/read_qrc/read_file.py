﻿# -*- coding: utf-8 -*-
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from static import style_rc


_author_ = 'luwt'
_date_ = '2020/10/9 17:01'


def read_file(file_path):
    file = QFile(file_path)
    # 确定是读取文本文件，并且自动把换行符修改为 '\n'
    file.open(QIODevice.ReadOnly | QIODevice.Text)
    content = QTextStream(file).readAll()
    file.close()
    return content


def read_qss():
    return read_file(":/style.qss")
