#   Author: Matthew Gerola
#   Class: CptS 455 HW #3
#   Date October 14, 2023

import socket
import threading
import sys
import os

files = socket.socket()
messages = socket.socket()

def messages_read():
    while(True):
        data = m_connection.recv(1024)
        while(data):
            print("Client: " + data.decode())
            data = False


def files_read():
    while(True):
        data = f_connection.recv(1024)
        contents = "Test".encode()
        while(data):
            with open(data.decode(),"w") as new_file:
                while(True):
                    contents = f_connection.recv(1024)
                    while(contents):
                        new_file.write(contents.decode())
                        contents = False
                        continue
                    if contents == False:
                        break
            data = False
            print("New File collected from the Client")
            m_connection.sendall("New File gotten from the client".encode())


def send_data(file_name):
    contents = os.listdir()
    if file_name in contents:
        f_connection.sendall(file_name.encode())#send the title of the file
        print("Sending data to the Client...")
        m_connection.sendall("Sending data to the Client...".encode())
        with open(file_name,"r") as sending_data:#send the contents of the data to the server for the files contents
            content = sending_data.read()
            f_connection.sendall(content.encode())
    else:
        print("This file does not exist..")
        return False


port_messages = 9999
port_files = 10000

files.bind(('127.0.0.1',port_files))
messages.bind(('127.0.0.1',port_messages))

files.listen(1)
messages.listen(1)

f_connection, f_address = files.accept() #Get a new Connection
m_connection, m_address = messages.accept() #Get a new Connection

messages_thread = threading.Thread(target=messages_read,args=())
messages_thread.setDaemon(True)
messages_thread.start()


files_thread = threading.Thread(target=files_read,args=())
files_thread.setDaemon(True)
files_thread.start()


while(m_connection and f_connection):
    command = input()
    check = command.split()
    if check[0] != "Message" and check[0] != "message" and check[0] != "File" and check[0] != "file" and check[0] != "exit":
        print("Please specify Message or Send.\n")
        continue
    elif check[0] == "Message" or check[0] == "message":
        content = " ".join(check[1:])
        m_connection.sendall(content.encode())
    elif check[0] == "File" or check[0] == "file":
        send_data(check[1])
    elif check[0] == "exit":
        m_connection.close()
        f_connection.close()
        sys.exit()
        break

m_connection.close()
f_connection.close()