# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal

from src.ssh_func.ssh_inter import SSHConnect

_author_ = 'luwt'
_date_ = '2020/10/10 11:20'


class SSHConnectWorker(QThread):

    error = pyqtSignal(Exception)
    result = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            self.produce(self.consume())
        except Exception as e:
            self.error.emit(e)

    def consume(self):
        while True:
            n = yield
            self.result.emit(n)

    def produce(self, consumer):
        consumer.__next__()
        self.connect = SSHConnect('centos121', 22, 'root', 'admin', consumer)
        consumer.close()

