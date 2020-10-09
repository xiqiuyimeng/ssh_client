# -*- coding: utf-8 -*-
import paramiko
from src.ssh_func import interactive

_author_ = 'luwt'
_date_ = '2020/10/9 11:50'


# 记录日志
paramiko.util.log_to_file('./test')
# 建立ssh连接
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('centos121', port=22, username='root', password='admin', compress=True)
# 建立交互式shell连接
channel = ssh.invoke_shell()
# 建立交互式管道
interactive.interactive_shell(channel)
# 关闭连接
channel.close()
ssh.close()
