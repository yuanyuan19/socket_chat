import socket
import threading
from process import *

server_port=9092
over=[]

#某个函数操控全局变量的时候锁住
lock_func=threading.Lock()


def thread_send_function(ip_port,server_socket):
    #不断判断消息队列中有没有发给ip_port的消息，判断当前客户端是否结束
    while ip_port not in over:
        lock_func.acquire
        mail_list= get_mails_filter(ip_port)
        lock_func.release
        for i in mail_list:
            lock_func.acquire
            del_mails(i)
            lock_func.release
            (sender,receiver,mail)=i #解包赋值
            message=sender+': '+mail
            server_socket.send(message.encode('gbk'))
    #把ip_port从over里删除
    over.remove(ip_port)

def thread_recv_function(ip_port,server_socket):
    print("Connected with",*ip_port)
    #设置用户名初始化
    lock_func.acquire
    add_mail("server",ip_port,"set your name please:")
    lock_func.release
    try:
        message = server_socket.recv(1024)
        lock_func.acquire
        add_user(ip_port,message.decode('gbk'))
        add_mail("server",ip_port,"let's start chatting!")
        lock_func.release
        if DEBUG:
            print(ip_port,":",message.decode('gbk'))
    except (ConnectionResetError, ConnectionAbortedError):
        print("disconnected with:",*ip_port)
        over.append(ip_port)
    else:
        #正常收消息并处理
        while True:
            try:
                message = server_socket.recv(1024)
            except (ConnectionResetError, ConnectionAbortedError):
                print("disconnected with:",*ip_port)
                over.append(ip_port)
                break
            else:
                if message:
                    #处理收到的message
                    lock_func.acquire
                    process(message,ip_port)
                    lock_func.release
                else:
                    #结束这个服务器的线程 其实每次客户端都是强制断开，所以走的是抛异常的路
                    print("disconnected with:",*ip_port)
                    over.append(ip_port)
                    break
    finally:
        server_socket.close()
        #清空全局变量里有关该客户端的内容
        lock_func.acquire
        mail_list= get_mails_filter(ip_port)
        lock_func.release
        for i in mail_list:
            lock_func.acquire
            del_mails(i)
            lock_func.release
        lock_func.acquire
        del_member_from_rooms(get_user_name(ip_port))
        delete_user(get_user_name(ip_port))
        lock_func.release
        if DEBUG:
            print(rooms,users)



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
server_socket.bind(("", server_port))
server_socket.listen(128)

while True:
    new_client, ip_port = server_socket.accept()

    thread_send=threading.Thread(target=thread_send_function, args=(ip_port,new_client),daemon=True)
    thread_recv=threading.Thread(target=thread_recv_function, args=(ip_port,new_client),daemon=True)
    thread_send.start()
    thread_recv.start()