# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:49:43 2018

@author: aakash.chotrani
"""
from PIL import Image
from PIL import ImageFile
import socket                   # Import socket module
import io

ImageFile.LOAD_TRUNCATED_IMAGES = True

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
print(s)
host = socket.gethostname()     # Get local machine name
print('host name:',host)
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.


def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    Image_Size = 0
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
        Image_Size += 4096
        print(Image_Size)
    return data

print ('Server listening....')
thanks_message = 'Thank you for connecting'
while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
#
#    filename='mytext.txt'
#    f = open(filename,'rb')
#    l = f.read(1024)
#    while (l):
#       conn.send(l)
#       print('Sent ',repr(l))
#       l = f.read(1024)
#    f.close()
    
    print("Server received an Image from client")
    counter = 1
#    buffer = conn.recv(4096000000)
    buffer = recvall(conn)
#    while conn.recv(512) != b'':
#        print('\n Buffer Received',counter)
#        if (counter == 1):
#            buffer = conn.recv(512)
#        else:
#            buffer += conn.recv(512)
#            
#        if not buffer:
#            break
#        counter = counter + 1
##        print(buffer)
    image = Image.open(io.BytesIO(buffer))
    image.show()
    image.save('server_img.jpg')
    
    

#    print('Done sending')
#    conn.sendto(thanks_message.encode(),(host,port))
#    conn.close()