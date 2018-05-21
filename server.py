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
host = socket.gethostname()     # Get local machine name
print('host name:',host)
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')
thanks_message = 'Thank you for connecting'
while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    data = conn.recv(8192)
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
    image = Image.open(io.BytesIO(data))
    image.show()
    image.save('server_img.png')
    

#    print('Done sending')
    conn.sendto(thanks_message.encode(),(host,port))
    conn.close()