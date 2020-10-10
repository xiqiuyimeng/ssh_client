# -*- coding: utf-8 -*-
_author_ = 'luwt'
_date_ = '2020/10/9 11:49'

import socket
import sys
# windows does not have termios...
try:
    import termios
    import tty
    has_termios = True
except ImportError:
    has_termios = False


def interactive_shell(chan, consumer):
    if has_termios:
        posix_shell(chan, consumer)
    else:
        windows_shell(chan, consumer)


def posix_shell(chan, consumer):
    import select
    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)
        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)


def windows_shell(chan, consumer):
    import threading
    def writeall(sock):
        while True:
            data = sock.recv(1024)
            if not data:
                break
            consumer.send(data.decode('utf8'))
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()
    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)
    except EOFError:
        pass
