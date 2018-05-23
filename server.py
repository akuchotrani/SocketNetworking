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
        if part == b'':
            break
        Image_Size += 4096
#        print(Image_Size)
    return data

print ('Server listening....')
thanks_message = 'Thank you for connecting'
server_img_counter = 0
while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    
    print("Server received an Image from client")
    counter = 1
    buffer = recvall(conn)

    image = Image.open(io.BytesIO(buffer))
    image.show()
    server_img_name = "server_"+str(server_img_counter) + ".jpg"
    print("saving image: ",server_img_name)
    image.save(server_img_name)
    server_img_counter = server_img_counter + 1
    
    

    print('Done Receiving')
    conn.sendto(thanks_message.encode(),(host,port))
    conn.close()