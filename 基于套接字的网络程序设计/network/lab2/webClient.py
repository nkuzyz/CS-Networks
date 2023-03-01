# lab2 用户端代码
import threading
from socket import *

# 需要访问的服务器地址
serverHOST = '192.168.3.131'  # 服务器地址 根据实际情况修改即可
# 服务器开放的端口
serverPORT = 9999
# 总共有多少个客户端线程发出请求
threadNum = 5
CODE = 'utf-8'
url = '/Web.html'

def send_data(rank):
    socketClient = socket(AF_INET, SOCK_STREAM)
    socketClient.connect((serverHOST, serverPORT))
    request_url = 'GET {} / HTTP/1.1\r\n' \
                  'Accept: text/html' \
                  'Host: {}\r\n ' \
                  'Connection: Close\r\n\r\n'.format(url, serverHOST + ':' + str(serverPORT))
    socketClient.send(request_url.encode(CODE))
    response = socketClient.recv(1024).decode()
    print('Client Number:', rank, '\nTCP Server reply:\n', response)
    print('=======================================================')
    socketClient.close()


def client():
    for rank in range(0, threadNum):
        p = threading.Thread(target=send_data, args=(rank,))
        p.start()
    pass


if __name__ == '__main__':
    client()
