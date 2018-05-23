# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:44:22 2018

@author: aakash.chotrani
"""

import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
print("client host name:",host)
port = 60000                    # Reserve a port for your service.

SERVER_IP = '10.10.33.58'
SERVER_HOST_NAME = 'dit2578us'
#ip_test = socket.gethostbyname(SERVER_HOST_NAME)
#print('IPTEST:',ip_test)
s.connect((SERVER_IP , port))
#message = "Hello from client"
#s.sendto(message.encode(),(host,port))

filename = 'meme.jpg'
image_file = open(filename,'rb')
image_size = 0;
while(True):
    data = image_file.read(4096)
    if not data:
        print('data is empty')
        break
    
    image_size += 4096
    print(image_size)
    
    
    print('sending image....')
    s.send(data)
#s.send(image_file.read())
image_file.close()
#    s.sendfile(image_file);
#print('Successfully get the file')
print('Successfully sent the file')
s.close()
print('connection closed')