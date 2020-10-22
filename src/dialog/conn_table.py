# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'static/ui/conn_tables.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QToolButton, QHeaderView, QMenu, QAction

from src.constant.constant import CONN_TABLE_HEADER_LABELS, CONNECT, EDIT, DELETE, EDIT_CONN_MENU, ADD_CONN_MENU
from src.dialog.conn_dialog import ConnDialog
from src.dialog.draggable_dialog import DraggableDialog
from src.func.operate_conn_thread import OperateConn
from src.scrollable_widget.scrollable_widget import MyTableWidget
from src.sys_info_db.conn_sqlite import ConnSqlite, Connection
from src.table.table_header import CheckBoxHeader
from src.table.table_item import MyTableWidgetItem


class ConnTableDialog(DraggableDialog):

    connect_signal = pyqtSignal(str)
    add_signal = pyqtSignal(Connection)
    edit_signal = pyqtSignal(int, Connection)
    del_signal = pyqtSignal(list)

    def __init__(self, parent, screen_rect):
        super().__init__()
        self.parent = parent
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
        self.tableWidget.itemSelectionChanged.connect(self.multi_select_func)
        # 双击
        self.tableWidget.doubleClicked.connect(
            lambda index: self.connect_ssh(self.tableWidget.item(index.row(), 1).text())
        )
        # 右击事件
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget.customContextMenuRequested.connect(self.right_click_menu)
        self.verticalLayout.addWidget(self.tableWidget)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.add_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.add_button.setObjectName("add_button")
        self.gridLayout.addWidget(self.add_button, 0, 0, 1, 1)
        self.del_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.del_button.setObjectName("del_button")
        self.gridLayout.addWidget(self.del_button, 0, 1, 1, 1)
        self.button_blank = QtWidgets.QLabel(self.conn_table_frame)
        self.button_blank.setObjectName("button_blank")
        self.gridLayout.addWidget(self.button_blank, 0, 2, 1, 1)
        self.button_blank2 = QtWidgets.QLabel(self.conn_table_frame)
        self.button_blank2.setObjectName("button_blank2")
        self.gridLayout.addWidget(self.button_blank2, 0, 3, 1, 1)
        self.quit_button = QtWidgets.QPushButton(self.conn_table_frame)
        self.quit_button.setObjectName("quit_button")
        self.gridLayout.addWidget(self.quit_button, 0, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.verticalLayout_frame.addWidget(self.conn_table_frame)

        self.add_button.clicked.connect(self.add_conn)
        self.del_button.clicked.connect(self.batch_delete)
        self.quit_button.clicked.connect(self.close)
        self.tableWidget.item_checkbox_clicked.connect(lambda checked, field, row:
                                                       self.on_checkbox_changed(checked, field, row))

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "连接列表"))
        self.conn_table_header.setText("连接列表")
        self.add_button.setText("添加连接")
        self.del_button.setText("删除连接")
        self.quit_button.setText("退出")
        self.button_blank.setText("")
        self.button_blank2.setText("")

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
        edit_act.triggered.connect(lambda: self.edit_conn(row, conn_name))
        menu.addAction(edit_act)
        del_act = QAction(self.icon, DELETE, self)
        del_act.triggered.connect(lambda: self.del_conn(row, conn_name))
        menu.addAction(del_act)
        tool_button.setMenu(menu)

    def right_click_menu(self, pos):
        """
        右键菜单功能，实现右键弹出菜单功能
        :param pos:右键的坐标位置
        """
        # 获取当前元素，只有在元素上才显示菜单
        item = self.tableWidget.itemAt(pos)
        if item:
            # 获取选中行号
            row = self.tableWidget.indexAt(pos).row()
            conn_name = item.text()
            # 生成右键菜单
            menu = QMenu()
            menu_names = [CONNECT, EDIT, DELETE]
            [menu.addAction(QAction(option, menu)) for option in menu_names]
            # 右键菜单点击事件
            menu.triggered.connect(lambda act: self.right_menu_func(act, row, conn_name))
            # 右键菜单弹出位置跟随焦点位置
            menu.exec_(QCursor.pos())

    def right_menu_func(self, act, row, conn_name):
        """右键菜单功能"""
        act_text = act.text()
        if act_text == CONNECT:
            self.connect_ssh(conn_name)
        elif act_text == EDIT:
            self.edit_conn(row, conn_name)
        elif act_text == DELETE:
            self.del_conn(row, conn_name)

    def connect_ssh(self, conn_name):
        self.connect_signal.emit(conn_name)
        self.close()

    def add_conn(self):
        connection = Connection(*((None,) * len(Connection._fields)))
        self.add_dialog = ConnDialog(connection, ADD_CONN_MENU, self.main_screen_rect)
        self.add_dialog.conn_signal.connect(self.add_table_row)
        self.add_dialog.exec()

    def add_table_row(self, connection):
        # 向主窗口发信号
        self.add_signal.emit(connection)
        # 表格添加行
        self.fill_table((connection, ), self.tableWidget.rowCount())

    def edit_conn(self, row, conn_name):
        connection = self.parent.conn_dict.get(conn_name)
        self.edit_dialog = ConnDialog(connection, EDIT_CONN_MENU, self.main_screen_rect)
        self.edit_dialog.conn_signal.connect(lambda conn: self.update_table(row, conn))
        self.edit_dialog.exec()

    def update_table(self, row, connection):
        # 先发射信号
        self.edit_signal.emit(row, connection)
        # 刷新表格，第一列和最后一列不需要填充
        conn = connection[1: 5]
        for col in range(self.tableWidget.columnCount() - 2):
            self.tableWidget.item(row, col + 1).setText(conn[col])
        # 菜单
        self.rebuild_pop_menu((row, ))

    def del_conn(self, row, conn_name):
        OperateConn(self, [(row, conn_name), ], self.del_signal)

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

    def batch_delete(self):
        if self.selected_connections:
            OperateConn(self, self.selected_connections, self.del_signal)

    def rebuild_pop_menu(self, rows):
        [self.tableWidget.setCellWidget(row, 5, self.make_tools(row)) for row in rows]
