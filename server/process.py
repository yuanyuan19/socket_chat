from model import *
import re

DEBUG=True

def process(message,ip_port):
    message=message.decode("gbk")

    #send message yuanyuan hello
    match=re.match(r'^send message (\w+(,\w+)*)\s+(.*)$', message)
    if match:
        receivers = match.group(1).split(',')
        message = match.group(3)
        for receiver in receivers:
            add_mail(get_user_name(ip_port),get_user_id_port(receiver),message)
        if DEBUG:
            print("send message",receivers,message)

    #list users
    match=re.match(r'^list users$', message)
    if match:
        users= ', '.join(get_users())
        add_mail("server",ip_port,users)
        if DEBUG:
            print("list users",users)

    #list rooms
    match=re.match(r'^list rooms$', message)
    if match:
        rooms= ', '.join(get_rooms())
        add_mail("server",ip_port,rooms)
        if DEBUG:
            print("list rooms",rooms)
    
    #create room room1 yuanyuan
    match=re.match(r'^create room (\w+)\s+([\w,]+)$',message)
    if match:
        room_name = match.group(1)
        members = match.group(2).split(',')
        create_rooms(room_name,members)
        if DEBUG:
            print("create room",room_name,members)

    #send room room1 hello
    match=re.match(r'^send room (\w+)\s+(.*)$',message)
    if match:
        room_name = match.group(1)
        message = match.group(2)
        for member in get_room_members(room_name):
            add_mail(room_name,get_user_id_port(member),message)
        if DEBUG:
            print("send room",room_name,message)
    

if __name__=="__main__":
    message="send room room1 hello"

    match = re.match(r'^send message (\w+(,\w+)*)\s+(.*)$', message)
    if match:
        receivers = match.group(1).split(',')
        message = match.group(3)
        print("Receivers:", receivers)
        print("Message:", message)
    

    match=re.match(r'^create room (\w+)\s+([\w,]+)$',message)
    if match:
        room_name = match.group(1)
        user_names = match.group(2).split(',')
        print("Room name:", room_name)
        print("User names:", user_names)

    match=re.match(r'^send room (\w+)\s+(.*)$',message)
    if match:
        room_name = match.group(1)
        message = match.group(2)
        print("Room name:", room_name)
        print("Message:", message)

