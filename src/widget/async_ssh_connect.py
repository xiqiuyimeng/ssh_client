# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal
from queue import Queue
from src.ssh_func.ssh_inter import SSHConnect

_author_ = 'luwt'
_date_ = '2020/10/10 11:20'


class SSHConnectWorker(QThread):

    error = pyqtSignal(Exception)
    result = pyqtSignal(str)

    def __init__(self, host, port, user, pwd):
        # 创建队列用以方便线程间数据交换
        self.queue = Queue()
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd

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
        self.connect = SSHConnect(self.host, self.port, self.user, self.pwd, consumer, self.queue)
        consumer.close()

    def send_cmd(self, cmd):
        self.queue.put(cmd)

