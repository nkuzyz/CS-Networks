# lab1 服务端代码
import random
from socket import *

# 创建一个UDP套接字(SOCK_DGRAM)
serverSocket = socket(AF_INET, SOCK_DGRAM)
# 绑定IP地址和端口号
Host = ''
serverSocket.bind((Host, 9999))

while True:
    print('==================2013747zyz==================')
    print('UDP Server is starting...')
    # 返回参数1和参数2之间的任意整数， 闭区间
    rand = random.randint(0, 10)
    # 服务端调用recvfrom()等待接收数据，此时阻塞
    message, address = serverSocket.recvfrom(1024)
    response = 'Wrong!'
    print("UDP Client {} makes a Ping request\n".format(address))
    if message == 'Ping'.encode("utf-8"):
        response = 'Pong'
    if rand < 4:  # 模拟丢失30%的客户端数据包
        print('Data lost')
        continue
    print('success')
    # 服务器接收到客户端发来的数据后，调用sendto()向客户发送应答数据
    serverSocket.sendto(response.encode("utf-8"), address)

serverSocket.close()
