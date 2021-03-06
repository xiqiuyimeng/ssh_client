# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'conn_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
"""
添加、编辑连接对话框界面
"""

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

from src.constant.constant import CONN_NAME, HOST, PORT, USER_NAME, PASSWORD, BUTTON_OK, BUTTON_CANCEL, \
    SAVE_CONN_SUCCESS_PROMPT, EDIT_CONN_MENU, ADD_CONN_MENU
from src.dialog.draggable_dialog import DraggableDialog
from src.func.conn_func import check_name_available
from src.sys_info_db.conn_sqlite import Connection, ConnSqlite
from src.widget.message_box import TimerMessageBox


class ConnDialog(DraggableDialog):

    conn_signal = QtCore.pyqtSignal(Connection)

    def __init__(self, connection, dialog_title, screen_rect):
        super().__init__()
        self.dialog_title = dialog_title
        self.connection = connection
        self._translate = QtCore.QCoreApplication.translate
        self.main_screen_rect = screen_rect
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.main_screen_rect.width() * 0.4, self.main_screen_rect.height() * 0.5)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.conn_frame = QtWidgets.QFrame(self)
        self.conn_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.conn_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.conn_frame.setObjectName("conn_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.conn_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.top_blank = QtWidgets.QLabel(self.conn_frame)
        self.top_blank.setText("")
        self.top_blank.setObjectName("top_blank")
        self.verticalLayout.addWidget(self.top_blank)
        self.title = QtWidgets.QLabel(self.conn_frame)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.under_title_first_blank = QtWidgets.QLabel(self.conn_frame)
        self.under_title_first_blank.setText("")
        self.under_title_first_blank.setObjectName("under_title_first_blank")
        self.verticalLayout.addWidget(self.under_title_first_blank)
        # 表格布局
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.conn_name = QtWidgets.QLabel(self.conn_frame)
        self.conn_name.setObjectName("conn_name")
        self.gridLayout.addWidget(self.conn_name, 0, 0, 1, 1)
        self.grid_layout_blank = QtWidgets.QLabel(self.conn_frame)
        self.grid_layout_blank.setText("")
        self.grid_layout_blank.setObjectName("grid_layout_blank")
        self.gridLayout.addWidget(self.grid_layout_blank, 0, 1, 1, 1)
        self.conn_name_value = QtWidgets.QLineEdit(self.conn_frame)
        self.conn_name_value.setObjectName("conn_name_value")
        self.gridLayout.addWidget(self.conn_name_value, 0, 2, 1, 1)
        self.name_check_splitter = QtWidgets.QSplitter(self.conn_frame)
        self.name_check_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.name_check_splitter.setObjectName("name_check_splitter")
        self.name_check_splitter.setHandleWidth(0)
        self.gridLayout.addWidget(self.name_check_splitter, 1, 2, 1, 1)
        self.name_check_pic = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_pic.setObjectName("name_check_pic")
        self.name_check_prompt = QtWidgets.QLabel(self.name_check_splitter)
        self.name_check_prompt.setObjectName("name_check_prompt")
        self.host = QtWidgets.QLabel(self.conn_frame)
        self.host.setObjectName("host")
        self.gridLayout.addWidget(self.host, 2, 0, 1, 1)
        self.host_value = QtWidgets.QLineEdit(self.conn_frame)
        self.host_value.setObjectName("host_value")
        self.gridLayout.addWidget(self.host_value, 2, 2, 1, 1)
        self.port = QtWidgets.QLabel(self.conn_frame)
        self.port.setObjectName("port")
        self.gridLayout.addWidget(self.port, 3, 0, 1, 1)
        self.port_value = QtWidgets.QLineEdit(self.conn_frame)
        self.port_value.setObjectName("port_value")
        self.gridLayout.addWidget(self.port_value, 3, 2, 1, 1)
        self.user = QtWidgets.QLabel(self.conn_frame)
        self.user.setObjectName("user")
        self.gridLayout.addWidget(self.user, 4, 0, 1, 1)
        self.user_value = QtWidgets.QLineEdit(self.conn_frame)
        self.user_value.setObjectName("user_value")
        self.gridLayout.addWidget(self.user_value, 4, 2, 1, 1)
        self.passwd = QtWidgets.QLabel(self.conn_frame)
        self.passwd.setObjectName("passwd")
        self.gridLayout.addWidget(self.passwd, 5, 0, 1, 1)
        self.passwd_value = QtWidgets.QLineEdit(self.conn_frame)
        self.passwd_value.setObjectName("passwd_value")
        self.gridLayout.addWidget(self.passwd_value, 5, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)
        self.bottom_blank = QtWidgets.QLabel(self.conn_frame)
        self.bottom_blank.setText("")
        self.bottom_blank.setObjectName("bottom_blank")
        self.verticalLayout.addWidget(self.bottom_blank)
        # 按钮
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.ok = QtWidgets.QPushButton(self.conn_frame)
        self.ok.setObjectName("ok")
        self.gridLayout_2.addWidget(self.ok, 0, 0, 1, 1)
        self.button_blank2 = QtWidgets.QLabel(self.conn_frame)
        self.button_blank2.setObjectName("button_blank2")
        self.gridLayout_2.addWidget(self.button_blank2, 0, 1, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.conn_frame)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout_2.addWidget(self.button_blank, 0, 2, 1, 1)
        self.cancel = QtWidgets.QPushButton(self.conn_frame)
        self.cancel.setObjectName("cancel")
        self.gridLayout_2.addWidget(self.cancel, 0, 3, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout_frame.addWidget(self.conn_frame)
        # 设置tab键的顺序
        self.setTabOrder(self.conn_name_value, self.host_value)
        self.setTabOrder(self.host_value, self.port_value)
        self.setTabOrder(self.port_value, self.user_value)
        self.setTabOrder(self.user_value, self.passwd_value)
        # 设置端口号只能输入数字
        self.port_value.setValidator(QtGui.QIntValidator())
        # 设置最多可输入字符数
        self.conn_name_value.setMaxLength(50)
        self.host_value.setMaxLength(20)
        self.user_value.setMaxLength(20)
        self.passwd_value.setMaxLength(30)

        self.conn_name_value.textEdited.connect(lambda conn_name: check_name_available(self, conn_name))
        self.conn_name_value.textEdited.connect(self.check_input)
        self.host_value.textEdited.connect(self.check_input)
        self.port_value.textEdited.connect(self.check_input)
        self.user_value.textEdited.connect(self.check_input)
        self.passwd_value.textEdited.connect(self.check_input)

        # 确定按钮：点击触发添加连接记录到系统库中，并增加到展示界面
        self.ok.clicked.connect(self.handle_func)
        # 确定按钮默认不可用，只有当输入框都有值才可用
        self.ok.setDisabled(True)
        # 取消按钮：点击则关闭对话框
        self.cancel.clicked.connect(self.close)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle(self._translate("Dialog", self.dialog_title))
        self.title.setText(self.dialog_title)
        self.conn_name.setText(CONN_NAME)
        self.host.setText(HOST)
        self.port.setText(PORT)
        self.user.setText(USER_NAME)
        self.passwd.setText(PASSWORD)
        # 按钮
        self.ok.setText(BUTTON_OK)
        self.cancel.setText(BUTTON_CANCEL)
        # 回显
        if self.connection.id:
            self.conn_name_value.setText(self._translate("Dialog", self.connection.name))
            self.host_value.setText(self._translate("Dialog", self.connection.host))
            port = str(self.connection.port) if self.connection.port else None
            self.port_value.setText(self._translate("Dialog", port))
            self.user_value.setText(self._translate("Dialog", self.connection.user))
            self.passwd_value.setText(self._translate("Dialog", self.connection.pwd))
            self.ok.setDisabled(False)
            self.button_blank.setDisabled(False)
            self.name_available = True
        else:
            self.port_value.setText(self._translate("Dialog", "22"))
            self.user_value.setText(self._translate("Dialog", "root"))

    def check_input(self):
        # 检查是否都有值
        conn = self.get_input()
        # 如果输入框都有值，那么就开放按钮，否则关闭
        if all(conn) and self.name_available:
            self.ok.setDisabled(False)
            self.button_blank.setDisabled(False)
        else:
            self.ok.setDisabled(True)
            self.button_blank.setDisabled(True)

    def get_input_connection(self):
        return Connection(self.connection.id, *self.get_input())

    def get_input(self):
        conn_name = self.conn_name_value.text()
        host = self.host_value.text()
        port = int(self.port_value.text())
        user = self.user_value.text()
        pwd = self.passwd_value.text()
        return conn_name, host, port, user, pwd

    def handle_func(self):
        """添加新的连接记录到系统库中，或编辑连接信息"""
        box_flag = False
        new_conn = self.get_input_connection()
        if self.dialog_title == EDIT_CONN_MENU:
            # 比较下是否有改动，如果有修改再更新库
            if set(new_conn[1:]) - set(self.connection[1:]):
                ConnSqlite().update_selective(new_conn)
                box_flag = True
        elif self.dialog_title == ADD_CONN_MENU:
            ConnSqlite().insert(new_conn)
            new_conn = ConnSqlite().select_latest_one()
            box_flag = True
        if box_flag:
            message_box = TimerMessageBox(self.dialog_title, SAVE_CONN_SUCCESS_PROMPT)
            message_box.exec_()
        self.close()
        self.conn_signal.emit(new_conn)
