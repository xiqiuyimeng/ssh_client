# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

from src.ssh_func.ssh_inter import ssh_connect

_author_ = 'luwt'
_date_ = '2020/10/10 11:20'


class SSHConnectWorker(QThread):

    error = pyqtSignal(Exception)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.produce(self.consume())
        except Exception as e:
            self.error.emit(e)

    def consume(self):
        count = 1
        while True:
            n = yield
            self.result.emit(count, n[0], n[1], n[2])
            count += 1

    def produce(self, consumer):
        consumer.__next__()
        ssh_connect(consumer)
        consumer.close()

