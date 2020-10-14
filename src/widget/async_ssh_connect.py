# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue
from src.ssh_func.ssh_inter import SSHConnect

_author_ = 'luwt'
_date_ = '2020/10/10 11:20'


class SSHConnectWorker(QThread):

    error = pyqtSignal(Exception)
    result = pyqtSignal(str)

    def __init__(self):
        # 创建队列用以方便线程间数据交换
        self.queue = Queue()
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
        self.connect = SSHConnect('centos121', 22, 'root', 'admin', consumer, self.queue)
        consumer.close()

    def send_cmd(self, cmd):
        self.queue.put(cmd)

