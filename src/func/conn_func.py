# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from src.constant.constant import CONN_NAME_AVAILABLE, CONN_NAME_EXISTS
from src.read_qrc.read_file import read_qss
from src.sys_info_db.conn_sqlite import ConnSqlite

_author_ = 'luwt'
_date_ = '2020/10/15 15:37'


def check_name_available(gui, conn_name):
    """检查名称是否可用"""
    label_height = gui.conn_name_value.geometry().height()
    gui.name_check_pic.setFixedWidth(label_height)
    if conn_name:
        name_available = ConnSqlite().check_name_available(gui.connection.id, conn_name)
        if name_available:
            prompt = CONN_NAME_AVAILABLE.format(conn_name)
            style = "color:green"
            # 重载样式表
            gui.conn_name_value.setStyleSheet(read_qss())
            pm = QPixmap(":/icon/right.png").scaled(label_height * 0.6,
                                                    label_height * 0.6,
                                                    Qt.IgnoreAspectRatio,
                                                    Qt.SmoothTransformation)
        else:
            prompt = CONN_NAME_EXISTS.format(conn_name)
            style = "color:red"
            gui.conn_name_value.setStyleSheet("#conn_name_value{border-color:red;color:red}")
            pm = QPixmap(":/icon/wrong.png").scaled(label_height * 0.6,
                                                    label_height * 0.6,
                                                    Qt.IgnoreAspectRatio,
                                                    Qt.SmoothTransformation)
        gui.name_available = name_available
        gui.name_check_pic.setPixmap(pm)
        gui.name_check_prompt.setStyleSheet(style)
        gui.name_check_prompt.setText(prompt)
