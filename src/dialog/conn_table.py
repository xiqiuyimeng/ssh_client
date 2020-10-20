# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'static/ui/conn_tables.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolButton, QHeaderView, QMenu, QAction

from src.constant.constant import CONN_TABLE_HEADER_LABELS, CONNECT, EDIT, DELETE
from src.dialog.draggable_dialog import DraggableDialog
from src.func.operate_conn_thread import OperateConn
from src.scrollable_widget.scrollable_widget import MyTableWidget
from src.sys_info_db.conn_sqlite import ConnSqlite
from src.table.table_header import CheckBoxHeader
from src.table.table_item import MyTableWidgetItem


class ConnTableDialog(DraggableDialog):

    connect_signal = pyqtSignal(str)
    edit_signal = pyqtSignal(int, str)
    del_signal = pyqtSignal(int, str)

    def __init__(self, screen_rect):
        super().__init__()
        self.main_screen_rect = screen_rect
        # 初始化需要使用的icon
        self.icon = QIcon(":/icon/exec.png")
        # 保存已经选择的连接，二维列表，子元素为元祖（表格的行，连接名称）
        self.selected_connections = list()
        self.setup_ui()

    def setup_ui(self):
        self.setObjectName("Dialog")
        # 当前窗口大小根据主窗口大小计算
        self.resize(self.main_screen_rect.width() * 0.6, self.main_screen_rect.height() * 0.6)
        # 不透明度
        self.setWindowOpacity(0.95)
        # 隐藏窗口边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置窗口背景透明
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.conn_table_frame = QtWidgets.QFrame(self)
        self.conn_table_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.conn_table_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.conn_table_frame.setObjectName("conn_table_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.conn_table_frame)
        self.verticalLayout.setObjectName("verticalLayout")

        self.conn_table_header = QtWidgets.QLabel(self.conn_table_frame)
        self.conn_table_header.setObjectName("conn_table_header")
        self.verticalLayout.addWidget(self.conn_table_header)
        # 添加表格
        self.tableWidget = MyTableWidget(self.conn_table_frame)
        self.tableWidget.setObjectName("tableWidget")
        # 表头
        self.make_table_header()
        # 填充表格数据
        self.fill_table(ConnSqlite().select_all())
        # 交替行颜色
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setAttribute(Qt.WA_TranslucentBackground, True)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        # 表格选中多行
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.doubleClicked.connect(lambda index: self.connect_ssh(self.tableWidget.item(index.row(), 1).text()))
        self.tableWidget.itemSelectionChanged.connect(self.multi_select_func)
        self.verticalLayout.addWidget(self.tableWidget)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.add_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.add_button.setObjectName("add_button")
        self.gridLayout.addWidget(self.add_button, 0, 0, 1, 1)
        self.edit_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.edit_button.setObjectName("edit_button")
        self.gridLayout.addWidget(self.edit_button, 0, 1, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.conn_table_frame)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout.addWidget(self.button_blank, 0, 2, 1, 1)
        self.del_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.del_button.setObjectName("del_button")
        self.gridLayout.addWidget(self.del_button, 0, 3, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.quit_button.setObjectName("quit_button")
        self.gridLayout.addWidget(self.quit_button, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_frame.addWidget(self.conn_table_frame)

        self.quit_button.clicked.connect(self.close)
        self.del_button.clicked.connect(self.batch_delete)
        self.tableWidget.item_checkbox_clicked.connect(lambda checked, field, row:
                                                       self.on_checkbox_changed(checked, field, row))

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "连接列表"))
        self.conn_table_header.setText("连接列表")
        self.add_button.setText("添加连接")
        self.edit_button.setText("编辑连接")
        self.del_button.setText("删除连接")
        self.quit_button.setText("退出")
        self.button_blank.setText("")

    def make_table_header(self):
        self.tableWidget.setColumnCount(6)
        # 实例化自定义表头
        self.table_header = CheckBoxHeader()
        self.table_header.setObjectName("table_header")
        self.tableWidget.setHorizontalHeader(self.table_header)
        self.tableWidget.setHorizontalHeaderLabels(CONN_TABLE_HEADER_LABELS)
        # 设置表头列宽度自动拉伸
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # 隐藏默认的行号
        self.tableWidget.verticalHeader().setHidden(True)
        self.table_header.select_all_clicked.connect(self.all_clicked)

    def fill_table(self, connections, start_row=0):
        connections = list(map(lambda conn: conn[1: 5], connections))
        for i, connection in enumerate(connections):
            if start_row:
                i += start_row
            self.tableWidget.insertRow(i)
            table_check_item = MyTableWidgetItem(self.tableWidget)
            table_check_item.setCheckState(Qt.Unchecked)
            table_check_item.setText(i + 1)
            self.tableWidget.setItem(i, 0, table_check_item)
            self.table_header.all_header_combobox.append(table_check_item)
            n = 1
            for field in connection:
                # 连接中的每一个字段
                if field is not None:
                    conn_item = MyTableWidgetItem(self.tableWidget)
                    conn_item.setText(field)
                    self.tableWidget.setItem(i, n, conn_item)
                    n += 1
            # 最后添加按钮，在序号为5的列
            self.tableWidget.setCellWidget(i, 5, self.make_tools(i))
        self.tableWidget.resizeRowsToContents()

    def make_tools(self, row):
        """
        添加操作按钮
        :param row: 当前行
        """
        tool_button = QToolButton(self)
        tool_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tool_button.setStatusTip('对连接的操作')
        tool_button.setPopupMode(QToolButton.InstantPopup)
        tool_button.setText('操作')
        tool_button.setIcon(self.icon)
        tool_button.setAutoRaise(True)
        self.pop_menu(tool_button, row)
        return tool_button

    def pop_menu(self, tool_button, row):
        conn_name = self.tableWidget.item(row, 1).text()
        menu = QMenu(self)
        connect_act = QAction(self.icon, CONNECT, self)
        connect_act.triggered.connect(lambda: self.connect_ssh(conn_name))
        menu.addAction(connect_act)
        edit_act = QAction(self.icon, EDIT, self)
        edit_act.triggered.connect(lambda: self.edit_emit(row, conn_name))
        menu.addAction(edit_act)
        del_act = QAction(self.icon, DELETE, self)
        del_act.triggered.connect(lambda: self.del_emit(row, conn_name))
        menu.addAction(del_act)
        tool_button.setMenu(menu)

    def connect_ssh(self, conn_name):
        self.connect_signal.emit(conn_name)
        self.close()

    def edit_emit(self, row, conn_name):
        self.edit_signal.emit(row, conn_name)

    def del_emit(self, row, conn_name):
        # OperateConn(self, self.selected_connections).handle_ui_delete(True, None)
        self.del_signal.emit(row, conn_name)

    def all_clicked(self, clicked):
        self.selected_connections.clear()
        if clicked:
            [self.selected_connections.append(
                (checkbox.row(), self.tableWidget.item(checkbox.row(), checkbox.column() + 1).text())
            ) for checkbox in self.table_header.all_header_combobox]
        self.table_header.change_state(clicked)

    def on_checkbox_changed(self, checked, conn_name, row):
        """点击复选框"""
        header_checked = False
        if checked and (row, conn_name) not in self.selected_connections:
            self.selected_connections.append((row, conn_name))
            # 与表头联动
            if len(self.selected_connections) == len(self.table_header.all_header_combobox):
                header_checked = True
        elif not checked and (row, conn_name) in self.selected_connections:
            self.selected_connections.remove((row, conn_name))
        self.table_header.set_header_checked(header_checked)

    def multi_select_func(self):
        # 处理选中内容
        indexes = self.tableWidget.selectedIndexes()
        selected_rows = set(map(lambda index: index.row(), indexes))
        for row in selected_rows:
            original_state = self.tableWidget.item(row, 0).checkState()
            if original_state == Qt.Unchecked:
                self.tableWidget.item(row, 0).setCheckState(Qt.Checked)
                self.on_checkbox_changed(Qt.Checked, self.tableWidget.item(row, 1).text(), row)
            elif original_state == Qt.Checked:
                self.tableWidget.item(row, 0).setCheckState(Qt.Unchecked)
                self.on_checkbox_changed(Qt.Unchecked, self.tableWidget.item(row, 1).text(), row)

    def batch_delete(self, selected_connections=None):
        OperateConn(self, selected_connections if selected_connections else self.selected_connections)

    def rebuild_pop_menu(self, rows):
        [self.tableWidget.setCellWidget(row, 5, self.make_tools(row)) for row in rows]
