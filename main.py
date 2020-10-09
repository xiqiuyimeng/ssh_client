# -*- coding: utf-8 -*-
import ctypes
import sys

from PyQt5 import QtWidgets

from src.main_window import MainWindow
from src.read_qrc.read_file import read_qss
from static import image_rc

_author_ = 'luwt'
_date_ = '2020/10/9 15:44'


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # 获取当前屏幕分辨率
    desktop = QtWidgets.QApplication.desktop()
    screen_rect = desktop.screenGeometry()
    app.setStyleSheet(read_qss())
    ui = MainWindow(screen_rect)
    # 声明AppUserModelID，否则windows认为这是python子程序，无法使用自定义任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ssh")
    ui.show()
    app.exec_()
    sys.exit()
