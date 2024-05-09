#! /usr/bin/env python
# -*- coding: UTF-8 -*- 
import socket
import time



# region
"""
# 创建socket对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 获取本地主机名和端口号
host = socket.gethostname()
print("server host: %s" % host)
port = 8888

# 将socket对象绑定到指定的主机和端口上
server_socket.bind((host, port))

# 开始监听连接
server_socket.listen(1)

# 等待客户端连接
print("等待客户端连接...")
client_socket, client_address = server_socket.accept()

print("连接来自: ", client_address)

# 接收客户端发送的数据
data = client_socket.recv(1024)

# 处理接收到的数据
print("接收到的数据为: ", data.decode())

# 发送响应数据给客户端
message = "欢迎连接到服务器!"
client_socket.send(message.encode())

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
# Host = socket.gethostname()
# print("HOST IP: %s" % Host)
# s.bind((HOST, Port))

s.bind((localhost, Port))
s.listen(1)

# HEADERSIZE = 10
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")

    clientsocket.send(bytes("Welcome to the server!", "utf-8"))
    
    # msg = "Welcome to the server!"
    # msg = f'{len(msg):<{HEADERSIZE}}' + msg
    # clientsocket.send(bytes(msg, "utf-8"))
    
    clientsocket.close()
"""
# endregion

# region
"""
import socket
import time

localhost = '127.0.0.1'
Port = 1234

# the code, socket with a fixed length header.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Host = socket.gethostname()
# print("HOST IP: %s" % Host)
# Port = 1234
# s.bind((Host, Port))
s.bind((localhost, Port))
s.listen(1)

HEADERSIZE = 10
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    # send msg to client + header('HEADERSIZE' spaces)!
    msg = "Welcome to the server!"
    msg = f'{len(msg):<{HEADERSIZE}}' + msg
    
    clientsocket.send(bytes(msg, "utf-8"))

    while True:
        time.sleep(3)
        msg = f" The time is! {time.time()}"
        msg = f'{len(msg):<{HEADERSIZE}}' + msg
        clientsocket.send(bytes(msg, "utf-8"))
"""
# endregion

# region
"""  
import pickle
# the code uses 'pickle'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Host = socket.gethostname()
print("HOST IP: %s" % Host)
Port = 1234
s.bind((Host, Port))
s.listen(1)

HEADERSIZE = 10
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established!")
    
    d = {1: "Hey", 2: "There"}
    msg = pickle.dumps(d)
    # print(msg)
    
    msg = bytes(f'{len(msg):<{HEADERSIZE}}', "utf-8") + msg
    
    clientsocket.send(msg)
"""
# endregion

# region
"""

# creat chat application with sockets in python 
# reference: Sentdex:` https://youtu.be/CV7_stUWvBQ?si=ppR4MQeKI5E5XNy5

import select

HEADER_LENGTH = 10
IP = '127.0.0.1'
PORT = 1234

# 创建一个TCP/IP套接字对象。socket.AF_INET表示使用IPv4地址族，socket.SOCK_STREAM表示使用流式套接字。
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
# 设置套接字选项，socket.SO_REUSEADDR：表示允许重用本地地址和端口。1：表示启用SO_REUSEADDR选项。
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()  

sockets_list = [server_socket]

clients = {}

print(f'Listening for connections  on {IP}:{PORT}...')


def receive_message(client_socket):
    # 该函数用于：按消息长度来接收信息，有效避免信息阻塞等问题
    try:
        # 接收Header of msgs（the header contains message of length)
        message_header = client_socket.recv(HEADER_LENGTH)
        
        # header为0 -》接收不到信息就关闭
        if not len(message_header):
            return False
        
        # 处理方法 和 client 发送的信息格式有关
        # 解析头部信息：strip()方法去除字符串两端的空白字符，然后转换Header -> int
        message_length = int(message_header.decode('utf-8').strip())
        print(message_length)
        
        # 返回破解后的msg
        return {'header':message_header, 'data': client_socket.recv(message_length)}
        
    except:
        # 接收不到信息就关闭
        return False
    
    
while True:
    # 使用select.select()函数来监视sockets_list中的套接字，并返回准备就绪的套接字列表read_sockets（包含server_socket）和 _不在意的列表 和 exception_sockets异常的列表。
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    # 挨个处理准备就绪的列表
    for notified_socket in read_sockets:
        # 当遇到 server_socket -》 处理新的客户端连接
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            
            user = receive_message(client_socket) # user 主要是 msg信息{’header','data'}
            
            if user is False:
                continue
            
            # 添加已接收的socket至 sockets_list
            sockets_list.append(client_socket)
            
            # 添加：notified_socker的用户到一个clients字典
            clients[client_socket] = user  # key-value
            
            print("Accepted new connection from {}:{}, username:{}".format(*client_address, user['data'].decode('utf-8')))
            
        else:
            # 处理已连接的客户端套接字：进一步删选
            message = receive_message(notified_socket)
            if message is False:
                print("Close connection from: {}".format(clients[notified_socket]['data'].decode('utf-8')))
                # 从sockets_list中移除有问题的notified_socket
                sockets_list.remove(notified_socket)
                
                # 删除
                del clients[notified_socket]
                
                continue
            
            # 处理指定socket的信息 
            user = clients[notified_socket]
            print(f'Received message from {user["data"].decode("utf-8")}: {message["data"].decode("utf-8")}')
            
            # 给client反馈
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user["header"] + user["data"] + message["header"] + message["data"])
                    
    # 异常socket处理：删除
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket] 
"""
# endregion

# region
"""
# 一个server对两个client
import socket
import threading

# 定义端口号
PORT1 = 1234
PORT2 = 5678

# 处理客户端连接的函数
def handle_client(client_socket):
    while True:
        # 接收客户端发送的数据
        data = client_socket.recv(1024)
        if not data:
            break
        
        # 处理接收到的数据
        # ...
        
        # 发送响应给客户端
        response = "Server response"
        client_socket.send(response.encode())

    # 关闭客户端连接
    client_socket.close()

# 创建套接字并绑定到两个端口上
localhost = '127.0.0.1'
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind((localhost, PORT1))
server_socket1.listen(1)

server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.bind((localhost, PORT2))
server_socket2.listen(1)

print(f"Server is listening on port {PORT1} and {PORT2}...")

# 处理客户端连接的函数
def accept_connections(server_socket):
    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")
        
        # 创建线程处理客户端连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# 创建线程分别处理两个端口的连接
thread1 = threading.Thread(target=accept_connections, args=(server_socket1,))
thread1.start()

thread2 = threading.Thread(target=accept_connections, args=(server_socket2,))
thread2.start()
"""
# endregion

# region
"""
# 定义两个server它们将接收同一个client的信息
import socket
import threading

# 定义端口号
PORT1 = 1234
PORT2 = 5678
localhost1 = "127.0.0.1"
localhost2 = "192.168.1.22"

# 处理客户端连接的函数
def handle_client(client_socket):
    while True:
        # 接收客户端发送的数据
        data = client_socket.recv(1024)
        if not data:
            break
        
        # 处理接收到的数据
        # ...
        
        # 发送响应给客户端
        response = f"{client_socket} : Server response"
        client_socket.send(response.encode())

    # 关闭客户端连接
    client_socket.close()

# 创建套接字并绑定到两个端口上
server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket1.bind((localhost1, PORT1))
server_socket1.listen(1)

server_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket2.bind((localhost2, PORT2))
server_socket2.listen(1)

print(f"Server is listening {localhost1} on port {PORT1} and {localhost2} on port {PORT2}...")

# 处理客户端连接的函数
def accept_connections(server_socket):
    while True:
        # 等待客户端连接
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")
        
        # 创建线程处理客户端连接
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

# 创建线程分别处理两个端口的连接
thread1 = threading.Thread(target=accept_connections, args=(server_socket1,))
thread1.start()

thread2 = threading.Thread(target=accept_connections, args=(server_socket2,))
thread2.start()

"""
# endregion
