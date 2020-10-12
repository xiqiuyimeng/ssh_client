# -*- coding: utf-8 -*-
from multiprocessing.pool import ThreadPool

_author_ = 'luwt'
_date_ = '2020/10/9 11:49'


class InteractiveShell:

    def __init__(self, channel, consumer):
        self.channel = channel
        self.consumer = consumer
        self.receiver = ThreadPool(2)
        self.receiver.apply_async(self.recv_msg)
        self.receiver.apply_async(self.send_cmd, args=("ll\n",))
        self.receiver.close()
        self.receiver.join()

    def recv_msg(self):
        while True:
            data = self.channel.recv(128)
            if not data:
                break
            self.consumer.send(data.decode())

    def send_cmd(self, cmd):
        self.channel.send(cmd)

