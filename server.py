#!/usr/bin/env python
from socket import*

try:
    input = raw_input
except:
    pass

def fuzz_den(meth):
    for encode in ("utf-8", "gbk", "iso8859-1"):
        try:
            return meth(encode)
        except Exception:
            continue

NORESP = b"\xff"
E = lambda I: fuzz_den(I.encode)
D = lambda I: fuzz_den(I.decode)

def enter_console(C):
    S, R = C.send, C.recv
    while 6:
        inputs = input("$> ")
        if inputs == "exit":
            break
        if S(E(inputs)) == 0:
            continue
        resp = R(4096*2)
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
        except:
            continue

if __name__ == "__main__":
    import sys
    server(*sys.argv[1].split(":"))
