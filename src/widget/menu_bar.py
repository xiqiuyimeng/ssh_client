# -*- coding: utf-8 -*-
"""
菜单栏列表生成
"""

from PyQt5 import QtGui, QtWidgets

_author_ = 'luwt'
_date_ = '2020/10/9 17:01'


def fill_menu_bar(gui):
    """
    填充菜单栏
    :param gui: 启动的主窗口界面对象
    """
    gui.file_menu = gui.menubar.addMenu("文件")
    gui.file_menu.setObjectName("file_menu")
    add_conn_menu(gui)
    ftp_menu(gui)
    exit_app_menu(gui)

    gui.help_menu = gui.menubar.addMenu("帮助")
    gui.help_menu.setObjectName("help_menu")
    help_menu(gui)
    about_menu(gui)


def add_conn_menu(gui):
    """
    添加连接菜单
    :param gui: 启动的主窗口界面对象
    """
    add_action = QtWidgets.QAction(QtGui.QIcon(':/icon/add.png'), "添加连接", gui)
    add_action.setShortcut('Ctrl+N')
    add_action.setStatusTip('在左侧列表中添加一条连接')
    # add_action.triggered.connect(lambda: add_conn_func(gui, gui.screen_rect))

    gui.file_menu.addAction(add_action)


def exit_app_menu(gui):
    """
    退出菜单
    :param gui: 启动的主窗口界面对象
    """
    exit_action = QtWidgets.QAction(QtGui.QIcon(':/icon/exit.png'), "退出程序", gui)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('退出应用程序')
    exit_action.triggered.connect(gui.close)

    gui.file_menu.addAction(exit_action)


def ftp_menu(gui):
    """
    文件传输菜单
    :param gui: 启动的主窗口界面对象
    """
    ftp_action = QtWidgets.QAction(QtGui.QIcon(':/icon/exec.png'), "文件传输", gui)
    ftp_action.setShortcut('Ctrl+G')
    ftp_action.setStatusTip('根据选择执行生成命令')
    # generate_action.triggered.connect(gui.generate)

    gui.file_menu.addAction(ftp_action)


def help_menu(gui):
    """帮助菜单"""
    help_action = QtWidgets.QAction(QtGui.QIcon(":/icon/add.png"), "帮助", gui)
    help_action.setShortcut('Ctrl+H')
    help_action.setStatusTip('帮助信息')
    # help_action.triggered.connect(gui.help)
    gui.help_menu.addAction(help_action)


def about_menu(gui):
    """关于菜单"""
    about_action = QtWidgets.QAction(QtGui.QIcon(":/icon/exit.png"), "关于", gui)
    about_action.setStatusTip('关于')
    # about_action.triggered.connect(gui.about)
    gui.help_menu.addAction(about_action)
