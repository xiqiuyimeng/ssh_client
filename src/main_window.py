# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout

from src.widget.menu_bar import fill_menu_bar
from src.widget.scrollable_widget import MyTextEdit
from src.widget.title_bar import TitleBar
from src.widget.tool_bar import fill_tool_bar


class MainWindow(QMainWindow):

    def __init__(self, screen_rect):
        super().__init__()
        # 当前屏幕的分辨率大小
        self.desktop_screen_rect = screen_rect
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

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.setFixedWidth(self.desktop_screen_rect.width() / 10)
        self.horizontalLayout.addWidget(self.listWidget)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "Tab 1")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "Tab 2")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setObjectName("menubar")
        fill_menu_bar(self)

        # 创建标题栏
        self.title_bar = TitleBar(30, self, self.menubar)
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setFixedWidth(self.width())

        # 工具栏
        self.toolBar = QtWidgets.QToolBar(self)
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
        self.set_up_tab()

        self.tabWidget.tabCloseRequested.connect(self.close_tab)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Linux连接工具"))

    def close_tab(self, tab_index):
        self.tabWidget.removeTab(tab_index)

    def set_up_tab(self):
        tab = self.tab
        verticalLayout_scroll = QtWidgets.QHBoxLayout(tab)
        verticalLayout_scroll.setObjectName("verticalLayout_scroll")
        tab.text_edit = MyTextEdit(tab)
        tab.text_edit.setObjectName("text_edit")
        # 以纯文本形式显示
        tab.text_edit.setPlainText("test")
        verticalLayout_scroll.addWidget(tab.text_edit)

