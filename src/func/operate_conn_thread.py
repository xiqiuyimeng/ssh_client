# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

from src.constant.constant import OPERATION_FAILED, DEL_CONN
from src.sys_info_db.conn_sqlite import ConnSqlite
from src.widget.loading_widget import LoadingMask
from src.widget.message_box import pop_fail

_author_ = 'luwt'
_date_ = '2020/9/21 16:35'


class OperateConnWorker(QThread):

    result = pyqtSignal(bool, object)

    def __init__(self, selected_conns):
        super().__init__()
        self.selected_conns = selected_conns

    def run(self):
        try:
            self.batch_delete_template()
        except Exception as e:
            self.result.emit(False, f'{OPERATION_FAILED}\t\n {e}')

    def batch_delete_template(self):
        ConnSqlite().batch_delete(self.selected_conns)
        self.result.emit(True, None)


class OperateConn:

    def __init__(self, gui, selected_conns):
        # 调用者
        self.gui = gui
        self.loading_mask = LoadingMask(self.gui, ":/gif/loading.gif")
        self.loading_mask.show()
        self.selected_conns = selected_conns
        self.operate_conn()

    def operate_conn(self):
        self.worker = OperateConnWorker(list(map(lambda x: x[1], self.selected_conns)))
        self.worker.result.connect(lambda flag, result: self.handle_ui_delete(flag, result))
        self.worker.start()

    def handle_ui_delete(self, flag, result):
        if flag:
            self.loading_mask.close()
            delete_rows = sorted(list(map(lambda x: x[0], self.selected_conns)), reverse=True)
            # 已经删除完毕，选中列表可以清除
            self.selected_conns.clear()
            # 删除全选框中的元素
            [self.gui.table_header.all_header_combobox.remove(self.gui.tableWidget.item(row, 0))
             for row in delete_rows]
            # 删除页面行
            [self.gui.tableWidget.removeRow(row) for row in delete_rows]
            self.gui.table_header.set_header_checked(False)
            # 最后一个是最小的行号，在这个行号以后都需要调整
            min_row = delete_rows[-1]
            need_update = (list(range(self.gui.tableWidget.rowCount())))[min_row:]
            if need_update:
                [self.gui.tableWidget.item(row, 0).setText(row + 1) for row in need_update]
                # 重新构建事件
                self.gui.rebuild_pop_menu(need_update)
        else:
            pop_fail(DEL_CONN, result)

