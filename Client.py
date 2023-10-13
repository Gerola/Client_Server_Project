#   Author: Matthew Gerola
#   Class: CptS 455 HW #3
#   Date October 14, 2023

import socket
import threading
import sys
import os

files = socket.socket()         #Files socket
messages = socket.socket()      #Messages socket 

def messages_read():
    while(True):
        data = messages.recv(1024)
        while(data):
            print("Server: " + data.decode())
            data = False


def files_read():
    while(True):
        data = files.recv(1024)
        contents = True
        while(data):
            with open(data.decode(),"w") as new_file:
                while(True):
                    contents = files.recv(1024)
                    while(contents):    
                        new_file.write(contents.decode())
                        contents = False
                        continue
                    if contents == False:
                        break

            data = False
            print("New File gotten from the Server")
            messages.sendall("New File gotten from the Server".encode())



                    
def send_data(file_name):
    contents = os.listdir()
    if file_name in contents:
        files.sendall(file_name.encode())#send the title of the file
        print("Sending Data to the Server...")
        messages.sendall("Sending Data to the Server".encode())
        with open(file_name,"r") as sending_data:#send the contents of the data to the server for the files contents
            content = sending_data.read()
            files.sendall(content.encode())
    else:
        print("This file does not exist..")
        return False

port_message = 9998             #New Port Number for message
port_file = 9997                #New Port Number for file

files.bind(('127.0.0.1',port_file))           #bind the ports
messages.bind(('127.0.0.1',port_message))      #bind the ports

files.connect(('127.0.0.1', 10000)) #Connect to the Server
print("Connected to the Server for File Transfer")
messages.connect(('127.0.0.1', 9999))#Connect to the Server
print("Connected to the Server for Message Transfer")

files_thread = threading.Thread(target=files_read,args=())
files_thread.setDaemon(True)
files_thread.start()

messages_thread = threading.Thread(target=messages_read,args=())
messages_thread.setDaemon(True)
messages_thread.start()

print("Type Message then the message to send message\nor\nFile with the file name, to send a file to the server: \n\n")
    
while(True):
    command = input()
    check = command.split()
    if check[0] != "Message" and check[0] != "message" and check[0] != "File" and check[0] != "file" and check[0] != "exit":
        print("Please specify Message or File.\n")
        continue
    elif check[0] == "Message" or check[0] == "message":
        content = " ".join(check[1:])
        messages.sendall(content.encode())
    elif check[0] == "File" or check[0] == "file":
        send_data(check[1])
    elif check[0] == "exit":
        messages.close()
        files.close()
        sys.exit()
        break