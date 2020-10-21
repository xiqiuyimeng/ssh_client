# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout

from src.constant.constant import ADD_CONN_MENU, CONN_LIST, EDIT_CONN_MENU, CONN_INFO
from src.dialog.conn_dialog import ConnDialog
from src.dialog.conn_table import ConnTableDialog
from src.dialog.rename_dialog import RenameDialog
from src.draggable_widget.draggable_ancestors_widget import DragWindowToolBar
from src.func.list_func import add_list_item, show_all_item, right_click_menu, rename_list_item, delete_list_item, \
    update_list_item
from src.sys_info_db.conn_sqlite import Connection
from src.widget.async_ssh_connect import SSHConnectWorker
from src.widget.menu_bar import fill_menu_bar
from src.widget.scrollable_widget import MyTextEdit, MyListWidget
from src.widget.title_bar import TitleBar
from src.widget.tool_bar import fill_tool_bar


class MainWindow(QMainWindow):

    def __init__(self, screen_rect):
        super().__init__()
        # 当前屏幕的分辨率大小
        self.desktop_screen_rect = screen_rect
        # 保存下已有的连接, conn_name: connection
        self.conn_dict = dict()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setObjectName("MainWindow")
        self.resize(self.desktop_screen_rect.width() * 0.6, self.desktop_screen_rect.height() * 0.7)
        # 当前窗口的分辨率大小，其他窗口以此为参考
        self.screen_rect = self.geometry()

        # 创建主控件，用以包含所有内容
        self.main_widget = QtWidgets.QWidget()
        # 主控件中的布局
        self.main_layout = QVBoxLayout()
        # 设置所有间距为0
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.horizontal_splitter = QtWidgets.QSplitter(self.centralwidget)
        self.horizontal_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.horizontal_splitter.setObjectName("horizontal_splitter")

        self.left_widget = QtWidgets.QWidget(self.horizontal_splitter)
        self.left_widget.setObjectName("left_widget")
        self.verticalLayout_left = QtWidgets.QVBoxLayout(self.left_widget)
        self.list_header = QtWidgets.QLabel(self.left_widget)
        self.list_header.setObjectName("list_header")
        self.verticalLayout_left.addWidget(self.list_header)
        self.listWidget = MyListWidget(self.left_widget)
        self.listWidget.setObjectName("listWidget")
        self.set_up_list()
        self.verticalLayout_left.addWidget(self.listWidget)

        self.tabWidget = QtWidgets.QTabWidget(self.horizontal_splitter)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        # 默认隐藏
        self.tabWidget.hide()
        # 设置分割器左右比例
        self.horizontal_splitter.setStretchFactor(0, 1)
        self.horizontal_splitter.setStretchFactor(1, 5)
        self.horizontalLayout.addWidget(self.horizontal_splitter)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setObjectName("menubar")
        fill_menu_bar(self)

        # 创建标题栏
        self.title_bar = TitleBar(30, self, self.menubar)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setFixedWidth(self.width())

        # 工具栏
        self.toolBar = DragWindowToolBar(self)
        self.toolBar.setObjectName("toolBar")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        fill_tool_bar(self)
        self.toolBar.setIconSize(QSize(50, 40))
        # 设置名称显示在图标下面（默认本来是只显示图标）
        self.toolBar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        # 主布局添加所有部件，依次为标题栏、菜单栏、工具栏、承载了实际窗口内容的主控件，将窗口中央控件设置为包含所有的控件
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.toolBar)
        self.main_layout.addWidget(self.centralwidget)
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()

        self.tabWidget.tabCloseRequested.connect(self.close_tab)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Linux连接工具"))
        self.list_header.setText(CONN_LIST)

    def set_up_list(self):
        self.listWidget.setIconSize(QSize(40, 30))
        self.list_icon = QIcon(":/icon/mysql_conn_icon.png")
        self.listWidget.itemDoubleClicked.connect(lambda item: self.connect(item.text()))
        # 右击事件
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(lambda pos: right_click_menu(self, pos))
        # 选中
        self.listWidget.itemSelectionChanged.connect(self.set_up_conn_info)
        # 展示列表
        show_all_item(self)

    def set_up_conn_info(self):
        # 获取当前选中元素的连接名
        if self.listWidget.currentItem():
            conn_name = self.listWidget.currentItem().text()
            connection = self.conn_dict.get(conn_name)
            if not hasattr(self, "conn_info_label"):
                self.conn_info_label = QtWidgets.QLabel(self.left_widget)
            self.conn_info_label.setText(CONN_INFO.format(*connection[1:5]))
            self.verticalLayout_left.addWidget(self.conn_info_label)
        else:
            if hasattr(self, "conn_info_label"):
                self.conn_info_label.hide()

    def close_tab(self, tab_index):
        self.tabWidget.removeTab(tab_index)
        if not self.tabWidget.count():
            self.tabWidget.hide()

    def set_up_tab(self, connection):
        # 恢复tab控件可见性
        self.tabWidget.show()
        tab = QtWidgets.QWidget()
        self.tabWidget.addTab(tab, connection.name)
        verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        verticalLayout_scroll.setContentsMargins(0, 0, 0, 0)
        tab.text_edit = MyTextEdit(tab)
        tab.text_edit.setObjectName("text_edit")
        verticalLayout_scroll.addWidget(tab.text_edit)
        connect_thread = SSHConnectWorker(*connection[2:])
        # 输出界面，以纯文本形式显示
        connect_thread.result.connect(lambda msg: tab.text_edit.append_plain_text(msg))
        tab.text_edit.cmd_signal.connect(lambda cmd: connect_thread.send_cmd(cmd))
        connect_thread.start()
        setattr(tab, "connect_thread", connect_thread)

    def add_connection(self):
        conn_info = Connection(*((None,) * len(Connection._fields)))
        self.add_dialog = ConnDialog(conn_info, ADD_CONN_MENU, self.screen_rect)
        self.add_dialog.conn_signal.connect(lambda conn: add_list_item(self, conn))
        self.add_dialog.exec()

    def edit_connection(self, row, conn_name):
        connection = self.conn_dict.get(conn_name)
        self.edit_dialog = ConnDialog(connection, EDIT_CONN_MENU, self.screen_rect)
        self.edit_dialog.conn_signal.connect(lambda conn: update_list_item(self, row, conn))
        self.edit_dialog.exec()

    def rename_connection(self, row, old_conn_name):
        connection = self.conn_dict.get(old_conn_name)
        self.rename_dialog = RenameDialog(self.screen_rect, connection)
        self.rename_dialog.rename_result.connect(lambda conn_name: rename_list_item(self, row, conn_name))
        self.rename_dialog.exec()

    def connect(self, conn_name):
        connection = self.conn_dict.get(conn_name)
        self.set_up_tab(connection)

    def open_table(self):
        self.table_dialog = ConnTableDialog(self, self.screen_rect)
        self.table_dialog.connect_signal.connect(self.connect)
        self.table_dialog.edit_signal.connect(lambda row, conn: update_list_item(self, row, conn))
        self.table_dialog.del_signal.connect(lambda selected_conns:
                                             delete_list_item(self, selected_conns, del_data=False))
        self.table_dialog.exec()



