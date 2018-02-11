#!/usr/bin/env python
from socket import*

try:
    input = raw_input
except:
    pass

def server(h, p):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((h, int(p)))
    sock.listen(2)

    NOR = b"\xff"
    T = lambda I: I("utf-8")
    E = lambda I: T(I.encode)
    D = lambda I: T(I.decode)
    while 6:
        print("listen on %s:%s, waiting for connection." % (h, p))
        cli_sock, addr = sock.accept()
        S, R = cli_sock.send, cli_sock.recv
        print("connection from %s:%s" % addr)
        while 6:
            try:
                inputs = input("$> ")
                if inputs == "exit":
                    cli_sock.close()
                    break
                if S(E(inputs)):
                    response = R(1024)
                    if response != NOR:
                        print(D(response))
                        continue
                    print("$> !")
            except Exception:
                break

if __name__ == "__main__":
    import sys
    server(*sys.argv[1].split(":"))
