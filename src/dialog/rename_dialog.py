# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'static/ui/rename.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

from src.constant.constant import RENAME, BUTTON_OK, BUTTON_CANCEL
from src.dialog.draggable_dialog import DraggableDialog
from src.func.conn_func import check_name_available
from src.sys_info_db.conn_sqlite import ConnSqlite


class RenameDialog(DraggableDialog):

    rename_result = pyqtSignal(str)

    def __init__(self, screen_rect, connection):
        super().__init__()
        self.main_screen_rect = screen_rect
        self.connection = connection
        self.name_available = False
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        self.setFixedSize(self.main_screen_rect.width() * 0.3, self.main_screen_rect.height() * 0.25)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.rename_frame = QtWidgets.QFrame(self)
        self.rename_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.rename_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rename_frame.setObjectName("rename_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.rename_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rename_title = QtWidgets.QLabel(self.rename_frame)
        self.rename_title.setObjectName("rename_title")
        self.verticalLayout_2.addWidget(self.rename_title)
        self.conn_name_value = QtWidgets.QLineEdit(self.rename_frame)
        self.conn_name_value.setObjectName("conn_name_value")
        self.verticalLayout_2.addWidget(self.conn_name_value)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.name_check_splitter = QtWidgets.QSplitter(self.rename_frame)
        self.name_check_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.name_check_splitter.setObjectName("name_check_splitter")
        self.name_check_splitter.setHandleWidth(0)
        self.gridLayout.addWidget(self.name_check_splitter, 0, 0, 1, 2)
        self.name_check_pic = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_pic.setObjectName("name_check_pic")
        self.name_check_prompt = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_prompt.setObjectName("name_check_prompt")
        self.ok_button = QtWidgets.QPushButton(self.rename_frame)
        self.ok_button.setObjectName("ok_button")
        self.gridLayout.addWidget(self.ok_button, 1, 0, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(self.rename_frame)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout.addWidget(self.rename_frame)
        # 限制最多输入字符数
        self.conn_name_value.setMaxLength(50)
        self.conn_name_value.textEdited.connect(self.check_name_available)
        self.ok_button.setDisabled(True)
        self.ok_button.clicked.connect(self.rename)
        self.cancel_button.clicked.connect(self.close)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", RENAME))
        self.rename_title.setText(RENAME)
        self.ok_button.setText(BUTTON_OK)
        self.cancel_button.setText(BUTTON_CANCEL)

    def check_name_available(self, conn_name):
        check_name_available(self, conn_name)
        if self.name_available:
            self.ok_button.setDisabled(False)

    def rename(self):
        conn_name = self.conn_name_value.text()
        if conn_name != self.connection.name:
            ConnSqlite().rename_conn(self.connection.id, conn_name)
            self.rename_result.emit(conn_name)
            self.close()

