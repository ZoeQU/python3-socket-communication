#! /usr/bin/env python
# -*- coding: UTF-8 -*- 
from os import kill
import socket


# region
"""
# 创建socket对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取服务器的主机名和端口号
host = socket.gethostname()
print("client host: %s" % host)
port = 8888

# 连接到服务器
client_socket.connect((host, port))

# 发送消息给服务器
message = "Hello, 服务器!"
client_socket.send(message.encode())

# 接收服务器发送的响应数据
data = client_socket.recv(1024)

# 处理接收到的响应数据
print("接收到的数据为: ", data.decode())

# 关闭客户端连接
client_socket.close()
"""
# endregion

# region 
"""
import socket
import time

localhost = '127.0.0.1'
Port = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# s.connect((socket.gethostname(), 1234))
s.connect((localhost, Port))

full_msg = ''
while True:
    msg = s.recv(8)

    if len(msg) <= 0:
        break
    full_msg += msg.decode("utf-8")

print(full_msg)
""" 
# endregion

# region
"""
import socket
import time

localhost = '127.0.0.1'
Port = 1234

# the code, socket with a fixed length header.
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 1234))
s.connect((localhost, Port))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(16)
        # receive a msg w/ header
        if new_msg:
            print(f"new msg length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
            
        full_msg += msg.decode("utf-8")
        
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ''    
"""
# endregion
    
# region
"""  
import pickle

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = b''  #b for bytes
    new_msg = True
    while True:
        msg = s.recv(16)
        # receive a msg w/ header
        if new_msg:
            print(f"new msg length: {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
            
        full_msg += msg
        
        if len(full_msg) - HEADERSIZE == msglen:
            print("full msg recvd")
            print(full_msg[HEADERSIZE:])  # before decode 
            
            d = pickle.loads(full_msg[HEADERSIZE:])
            print(d)  # after decode
            
            new_msg = True
            full_msg = b'' 
"""
# endregion    

# region
"""
# creat chat application with sockets in python 
# reference: Sentdex:` https://youtu.be/CV7_stUWvBQ?si=ppR4MQeKI5E5XNy5

import select
import errno
import sys

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234
my_username = input("Username: ")  #输入用户名

#创建一个socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

# 将套接字设置为非阻塞模式，以实现非阻塞式的网络通信。
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
    # 输入用户要发送的信息msg
    message = input(f"my_username > ")
    
    if message:
        # 发送msg -> server  
        message = message.encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)
        
    try:
        while True:
            # 接收从server处发来的msg
            username_header = client_socket.recv(HEADER_LENGTH)
            
            if not len(username_header):
                print("Connection closed by the server")
                sys.exit()
                
            username_length = int(username_header.decode("utf-8").strip())
            username = client_socket.recv(username_length).decode("utf-8")
            
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode("utf-8").strip())
            message = client_socket.recv(message_length).decode("utf-8")
            
            print(f'{username} > {message}')
            
    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error: {}".format(str(e)))
            sys.exit()
            
            continue
    
    except Exception as e:
        print("Reading error: ".format(str(e)))
        sys.exit()
"""
# endregion                

# region
"""
# 两个client
import socket

# 定义服务器的IP和端口号
SERVER_IP = '127.0.0.1'
SERVER_PORT1 = 1234
SERVER_PORT2 = 5678

# 创建第一个客户端套接字并连接到服务器
client_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket1.connect((SERVER_IP, SERVER_PORT1))

# 发送数据给服务器
message1 = "Hello from client 1"
client_socket1.send(message1.encode())

# 接收服务器的响应
response1 = client_socket1.recv(1024)
print(f"Response from server: {response1.decode()}")

# 关闭客户端套接字
client_socket1.close()

# 创建第二个客户端套接字并连接到服务器
client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect((SERVER_IP, SERVER_PORT2))

# 发送数据给服务器
message2 = "Hello from client 2"
client_socket2.send(message2.encode())

# 接收服务器的响应
response2 = client_socket2.recv(1024)
print(f"Response from server: {response2.decode()}")

# 关闭客户端套接字
client_socket2.close()

"""
# endregion

# region 
"""

# 一个client将向两个server发出的信息
import socket


# 定义服务器的IP和端口号
localhost1 = "127.0.0.1"
localhost2 = "192.168.1.22"

SERVER_IP1 = localhost1
SERVER_PORT1 = 1234

SERVER_IP2 = localhost2
SERVER_PORT2 = 5678

# 创建第一个服务器的套接字并连接
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.connect((SERVER_IP1, SERVER_PORT1))

# 创建第二个服务器的套接字并连接
server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.connect((SERVER_IP2, SERVER_PORT2))

# 发送数据给第一个服务器
message1 = "Hello from client"
server_socket1.send(message1.encode())

# 接收第一个服务器的响应
response1 = server_socket1.recv(1024)
print(f"Response from server 1: {response1.decode()}")

# 发送数据给第二个服务器
message2 = "Hello from client"
server_socket2.send(message2.encode())

# 接收第二个服务器的响应
response2 = server_socket2.recv(1024)
print(f"Response from server 2: {response2.decode()}")

# 关闭套接字
server_socket1.close()
server_socket2.close()

"""
# endregion