import socket
import threading

ip="192.168.137.81"
port=9092
input_list=[]
client_over=[False]

#send会循环读取input_list,主线程会在input_list里放入消息
input_list_lock=threading.Lock()

def thread_send_function():
    while not client_over[0]:
        if len(input_list)!=0:
            message=input_list[0]
            input_list_lock.acquire()
            del input_list[0]
            input_list_lock.release()
            cilent_socket.send(message.encode('gbk'))

def thread_recv_function():
    while True:
        try:
            message = cilent_socket.recv(1024)
        except (ConnectionResetError, ConnectionAbortedError):
            #print("ConnectionResetError")
            client_over[0]=True
            break
        else:
            if message:
                print(message.decode('gbk'))

            else:
                #结束主进程 实际上服务器不会主动结束，应该不走这个逻辑
                #print("disconnected with:"+ip+" "+str(port))
                
                #要想访问必须得是引用赋值，可能不同线程之间的变量是共享的指针吧（乱猜）
                client_over[0]=True
                break

cilent_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    cilent_socket.connect((ip, port))
except Exception as result:
    print(result)
    pass
else:
    #连接成功后的逻辑
    print("connected with:"+ip+" "+str(port))
    thread_send=threading.Thread(target=thread_send_function, daemon=True)
    thread_recv=threading.Thread(target=thread_recv_function, daemon=True)
    thread_recv.start()
    thread_send.start()
    #线程创建好后执行循环
    while not client_over[0]:
        try:
            #断开连接后client_over[0]会被置为true，回车后解阻塞退出
            message=input()
        except KeyboardInterrupt:
            break
        else:
            input_list_lock.acquire()
            input_list.append(message)
            input_list_lock.release()
finally:
    #调用close方法是个好习惯
    cilent_socket.close()
    print("bye bye")