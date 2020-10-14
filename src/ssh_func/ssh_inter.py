# -*- coding: utf-8 -*-
import paramiko
from src.ssh_func import interactive

_author_ = 'luwt'
_date_ = '2020/10/9 11:50'


class SSHConnect:

    def __init__(self, host, port, user, pwd, consumer, queue):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.consumer = consumer
        self.queue = queue
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.connect()

    def connect(self):
        self.ssh_client.connect(self.host, self.port, self.user, self.pwd, compress=True)
        self.channel = self.ssh_client.invoke_shell()
        self.shell = interactive.InteractiveShell(self.channel, self.consumer, self.queue)
        self.channel.close()
        self.ssh_client.close()

