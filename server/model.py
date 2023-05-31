import threading

rooms={}
users={}
mail_queue=[]

#某个线程操控全局变量的时候锁住
lock=threading.Lock()

#users
def get_user_name(ip_port):
    with lock:
        for k,v in users.items():
            if v==ip_port:
                return k
        
def get_user_id_port(name):
    with lock:
        return users[name]

def get_users():
    with lock:
        return users.keys()

def add_user(ip_port,name):
    with lock:
        users[name]=ip_port

def delete_user(name):
    with lock:
        if name in users:
            del users[name]


#mails
def add_mail(sender,receiver,mail):
    with lock:
        mail_queue.append((sender,receiver,mail))
    #筛选发给这个ip_port的信息

def get_mails_filter(ip_port):
    with lock:
        mail_list=[]
        for i in range(len(mail_queue)):
                if mail_queue[i][1]==ip_port:
                    mail_list.append(mail_queue[i])
        return mail_list

def del_mails(mail):
    with lock:
        #总是搭配get_mails_filter使用，所以不用担心找不到
        mail_queue.remove(mail)


#rooms
def create_rooms(room_name,member_list):
    with lock:
        rooms[room_name]=member_list

def get_room_members(room_name):
    with lock:
        return rooms[room_name]

def get_rooms():
    with lock:
        return rooms.keys()

def del_member_from_rooms(name):
    with lock:
        empty_rooms=[]
        for room_name,members in rooms.items():
            if name in members:
                members.remove(name)
                if not members:
                    empty_rooms.append(room_name)
        for room_name in empty_rooms:
            del rooms[room_name]
    

if __name__=="__main__":
    #user
    add_user(("123.1",221),"yuanyuan")
    add_user(("123.1",222),"yuanyuan2")
    add_user(("123.1",223),"yuanyuan3")
    delete_user("yuanyuan")
    print(get_users())
    print(get_user_name(("123.1",223)))
    print(get_user_id_port("yuanyuan2"))
    add_user(("123.1",221),"yuanyuan")
    #mail
    add_mail("yuanyuan",("123.1",222),"你好啊笨比")
    add_mail("yuanyuan2",("123.1",221),"你好啊比")
    add_mail("yuanyuan2",("123.1",221),"你好笨比")
    print(get_mails_filter(("123.1",221)))
    del_mails(('yuanyuan2', ("123.1",221), '你好笨比'))
    #rooms
    create_rooms("room1",["yuanyuan","yvyv"])
    create_rooms("room2",["yuanyuan","yvyv","hh"])
    print(get_room_members("room1"))
    del_member_from_rooms("yuanyuan")
    print(get_room_members("room1"))
    del_member_from_rooms("yvyv")
    print(get_rooms())





