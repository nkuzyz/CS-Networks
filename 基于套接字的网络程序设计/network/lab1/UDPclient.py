# lab1 用户端代码
from socket import *
import time

serverHost = '192.168.3.131'  # 服务器地址 根据服务器地址进行修改即可
serverPort = 9999  # 服务器建立连接的端口号

clientSocket = socket(AF_INET, SOCK_DGRAM)  # 创建socket套接字
clientSocket.settimeout(1)  # 为socket设置时延为1秒

timeList = []  # 存放RTT
totalReq = 10  # 发送的报文总数
loseReq = 0  # 记录丢包数

print('UDP Client makes a Ping request to Server[%s:%d]  :' % (serverHost, serverPort))
for i in range(0, totalReq):
    start = time.perf_counter()  # RRT开始计数时间
    try:
        # 向服务器发送‘Ping’服务请求，将信息转换为byte后发送到指定服务器端
        clientSocket.sendto('Ping'.encode("utf-8"), (serverHost, serverPort))

        # 调用recvfrom()函数接收服务器发来的应答数据
        recvData, address = clientSocket.recvfrom(1024)
        # 超时处理，等到时间超过1秒，捕获抛出的异常后打印丢失报文，进行下一步操作
        RTT = (time.perf_counter() - start) * 1000
        # 存放RTT
        timeList.append(RTT)
        # 若服务器响应正常，收到‘Pong’
        if recvData.decode() == 'Pong':
            print('Num: %d reply from %s : time = %.5fms' % (i + 1, serverHost, RTT))
        else:
            print(recvData)
    # 若请求超时
    except Exception as e:
        loseReq += 1
        print('Num: %d out of time' % (i + 1))
# 关闭套接字
clientSocket.close()

print()
print('The Ping Message of %s :' % serverHost)
print('   UDP: sent = %d，got = %d，loss = %d (%d%% packet loss rate)' % (i + 1, i - loseReq + 1, loseReq, (loseReq / (i + 1)) * 100))
print("RTT_TIME(ms):")
try:
    print("   min_RRT = %.5fsms，max_RRT = %.5fsms，average_RRT = %.5fsms" % (min(timeList), max(timeList), sum(timeList)/len(timeList)))
except ValueError:
    print("   min_RRT = 0ms，max_RRT = 0ms，average_RRT = 0ms")