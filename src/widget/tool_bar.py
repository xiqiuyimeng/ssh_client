﻿# -*- coding: utf-8 -*-
"""
工具栏
"""

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

_author_ = 'luwt'
_date_ = '2020/10/9 17:01'


def fill_tool_bar(gui):
    add_insert_conn_tool(gui)
    add_ftp_tool(gui)
    add_close_list_tool(gui)
    add_open_list_tool(gui)
    add_open_table_tool(gui)
    add_exit_tool(gui)


def add_insert_conn_tool(gui):
    # 指定图标
    insert_tool = QAction(QIcon(':/icon/add.png'), '添加服务器信息', gui)
    insert_tool.setStatusTip('在左侧列表中添加一条服务器信息')
    insert_tool.triggered.connect(lambda: gui.add_connection())
    gui.toolBar.addAction(insert_tool)


def add_ftp_tool(gui):
    generate_tool = QAction(QIcon(':/icon/exec.png'), '文件传输', gui)
    generate_tool.setStatusTip('')
    # generate_tool.triggered.connect(gui.generate)
    gui.toolBar.addAction(generate_tool)


def add_close_list_tool(gui):
    close_tool = QAction(QIcon(':/icon/refresh.png'), '关闭连接列表', gui)
    close_tool.setStatusTip('关闭左侧的连接列表')
    close_tool.triggered.connect(gui.left_widget.hide)
    gui.toolBar.addAction(close_tool)


def add_open_list_tool(gui):
    open_tool = QAction(QIcon(':/icon/refresh.png'), '打开连接列表', gui)
    open_tool.setStatusTip('打开左侧的连接列表')
    open_tool.triggered.connect(gui.left_widget.show)
    gui.toolBar.addAction(open_tool)


def add_open_table_tool(gui):
    open_tool = QAction(QIcon(':/icon/refresh.png'), '打开连接表格', gui)
    open_tool.setStatusTip('打开左侧的连接列表')
    open_tool.triggered.connect(gui.open_table)
    gui.toolBar.addAction(open_tool)


def add_exit_tool(gui):
    exit_tool = QAction(QIcon(':/icon/exit.png'), '退出程序', gui)
    exit_tool.setStatusTip('退出应用程序')
    exit_tool.triggered.connect(gui.close)
    gui.toolBar.addSeparator()
    gui.toolBar.addAction(exit_tool)

