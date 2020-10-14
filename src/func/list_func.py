# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QListWidgetItem

from src.sys_info_db.conn_sqlite import ConnSqlite

_author_ = 'luwt'
_date_ = '2020/10/14 17:08'


def show_all_item(gui):
    """从数据库中查出所有项展示在页面"""
    [add_list_item(gui, connection) for connection in ConnSqlite().select_all()]


def add_list_item(gui, connection):
    """在页面添加一个项"""
    gui.listWidget.addItem(QListWidgetItem(gui.list_icon, connection.name))
    gui.conn_dict[connection.name] = connection

