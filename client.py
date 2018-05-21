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

with open('received_file.txt', 'wb') as f:
    print ('file opened')
#    while True:
#        print('receiving data...')
#        data = s.recv(1024)
#        print('data=%s', (data))
#        if not data:
#            break
#        # write data to a file
#        f.write(data)
    filename = 'meme.jpg'
    image_file = open(filename,'rb').read()
    s.send(image_file)
#    s.sendfile(image_file);
f.close()
#print('Successfully get the file')
print('Successfully sent the file')
s.close()
print('connection closed')