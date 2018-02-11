#!/usr/bin/env python
from socket import*

try:
    input = raw_input
except:
    pass

NORESP = b"\xff"
T = lambda I: I("utf-8")
E = lambda I: T(I.encode)
D = lambda I: T(I.decode)

def enter_console(C):
    S, R = C.send, C.recv
    while 6:
        inputs = input("$> ")
        if inputs == "exit":
            break
        if S(E(inputs)) == 0:
            continue
        resp = R(4096)
        if resp != NORESP:
            print(D(resp))
        else:
            print("$> !")

    C.close()

def server(h, p):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((h, int(p)))
    sock.listen(2)
    
    while 6:
        try:
            print("listen on %s:%s, waiting for connection." % (h, p))
            C, addr = sock.accept()
            print("connection from %s:%s" % addr)
            enter_console(C)
        except Exception:
            continue

if __name__ == "__main__":
    import sys
    server(*sys.argv[1].split(":"))
