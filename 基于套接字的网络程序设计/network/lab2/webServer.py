# lab2 服务端代码
import threading
import time
from socket import *

# 本机
HOST = ''  # 服务器地址 根据实际情况进行修改即可
# 开放的端口
PORT = 9999
# 成功请求的HTTP头部
head = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'+'Server:'+HOST+'-'+str(PORT)+'\r\n\r\n'
lock = threading.Lock()

def handle_client(connectionSocket, address):
    # 获取client请求的文件名及在本机sever上的路径
    lock.acquire()
    print("=================2013747zyz=======================")
    message = connectionSocket.recv(1024).decode()
    print("receive message time:", time.strftime("%Y-%m-%d %H:%M", time.localtime(time.perf_counter())), sep="")
    filename = message.split()[1]
    filepath = filename[1:]
    print('TCP Client', address, 'Request File: ', filepath)
    try:
        f = open(filepath)
        outputdata = head + f.read()
        f.close()
        connectionSocket.sendall(outputdata.encode())
        connectionSocket.close()
        print("Success!")
    except:
        print("[ERROR]The file being fetched is not existed.")
        with open("error.html", "r") as f:  # 异常则打开异常响应文件（404）
            outputdata = head + f.read()
        f.close()
        connectionSocket.sendall(outputdata.encode())
        connectionSocket.close()
        print("Wrong!")
    lock.release()

def server():
    # 准备服务器端socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # 连接
    serverSocket.bind((HOST, PORT))
    # 监听
    serverSocket.listen(10)
    print("TCP Server is listening...\n")
    while True:
        # 建立连接
        # 如果有新的客户端来链接服务端，那么就产生一个新的套接字专门为这个客户端服务
        # connectionSocket用来为这个客户端服务
        # serverSocket专门等待其他新的客户端连接
        connectionSocket, address = serverSocket.accept()
        # 设置线程，调用handle_client处理获取到的每一个用户端请求
        new_thread = threading.Thread(target=handle_client, args=(connectionSocket, address))
        # 启动线程
        new_thread.start()
    serverSocket.close()


if __name__ == '__main__':
    server()
