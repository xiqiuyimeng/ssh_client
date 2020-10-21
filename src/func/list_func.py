# -*- coding: utf-8 -*-
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidgetItem, QMenu, QAction

from src.constant.constant import CONNECT, EDIT, RENAME, DELETE
from src.sys_info_db.conn_sqlite import ConnSqlite, Connection

_author_ = 'luwt'
_date_ = '2020/10/14 17:08'


def show_all_item(gui):
    """从数据库中查出所有项展示在页面"""
    [add_list_item(gui, connection) for connection in ConnSqlite().select_all()]


def add_list_item(gui, connection):
    """在页面添加一个项"""
    gui.listWidget.addItem(QListWidgetItem(gui.list_icon, connection.name))
    gui.conn_dict[connection.name] = connection


def rename_list_item(gui, row, conn_name):
    """重命名"""
    old_name = gui.listWidget.item(row).text()
    gui.listWidget.item(row).setText(conn_name)
    new_conn = gui.conn_dict[old_name]._asdict()
    new_conn['name'] = conn_name
    gui.conn_dict[conn_name] = Connection(**new_conn)
    del gui.conn_dict[old_name]
    update_info_label(gui)


def update_list_item(gui, row, connection):
    """更新"""
    old_name = gui.listWidget.item(row).text()
    if old_name != connection.name:
        gui.listWidget.item(row).setText(connection.name)
        gui.conn_dict[connection.name] = connection
        del gui.conn_dict[old_name]
    else:
        gui.conn_dict[old_name] = connection
    update_info_label(gui)


def update_info_label(gui):
    if hasattr(gui, 'conn_info_label'):
        gui.set_up_conn_info()


def delete_list_item(gui, selected_conns, del_data=True):
    """删除项"""
    # 按行号逆序排序，由大到小，因为删除，需要从后向前删
    for row_conn_name in sorted(selected_conns, key=lambda x: x[0], reverse=True):
        if del_data:
            conn_id = gui.conn_dict.get(row_conn_name[1]).id
            ConnSqlite().delete(conn_id)
        del gui.conn_dict[row_conn_name[1]]
        gui.listWidget.takeItem(row_conn_name[0])


def right_click_menu(gui, pos):
    """
    右键菜单功能，实现右键弹出菜单功能
    :param gui: 主界面
    :param pos:右键的坐标位置
    """
    # 获取当前元素，只有在元素上才显示菜单
    item = gui.listWidget.itemAt(pos)
    if item:
        # 获取选中行号
        row = gui.listWidget.indexAt(pos).row()
        conn_name = item.text()
        # 生成右键菜单
        menu = QMenu()
        menu_names = [CONNECT, EDIT, RENAME, DELETE]
        [menu.addAction(QAction(option, menu)) for option in menu_names]
        # 右键菜单点击事件
        menu.triggered.connect(lambda act: right_menu_func(gui, act, row, conn_name))
        # 右键菜单弹出位置跟随焦点位置
        menu.exec_(QCursor.pos())


def right_menu_func(gui, act, row, conn_name):
    """右键菜单功能实现"""
    action_name = act.text()
    if action_name == CONNECT:
        gui.connect(conn_name)
    elif action_name == EDIT:
        gui.edit_connection(row, conn_name)
    elif action_name == RENAME:
        gui.rename_connection(row, conn_name)
    elif action_name == DELETE:
        delete_list_item(gui, ((row, conn_name), ))

