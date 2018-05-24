# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:49:43 2018

@author: aakash.chotrani
"""
import FaceRecognitionComplete

from PIL import Image
from PIL import ImageFile
import socket                   # Import socket module
import io
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

port = 60000                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
print(s)
host = socket.gethostname()     # Get local machine name
print('host name:',host)
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.


#####################################################################################
class Queue:

  def __init__(self):
      self.queue = list()

  def addtoq(self,dataval):
# Insert method to add element
      if dataval not in self.queue:
          self.queue.insert(0,dataval)
          return True
      return False
  
# Pop method to remove element
  def removefromq(self):
      if len(self.queue)>0:
          return self.queue.pop()
      return ("No elements in Queue!")
  
  def isEmpty(self):
      if(len(self.queue) == 0):
          return True
      else:
          return False


ImageReceivedQueue = Queue()
#####################################################################################
dir_server_image_dump = "ServerImages"
if not os.path.exists(dir_server_image_dump):
    print("creating server images folder")
    os.makedirs(dir_server_image_dump)


def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    Image_Size = 0
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        
        if part == b'':
            ImageReceivedQueue.addtoq(data)
            data = b''
            Image_Size = 0
            break
        
        
        Image_Size += 4096
        print(Image_Size)
        
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
    
    if(ImageReceivedQueue.isEmpty() == False):
        print("new image in the queue")
        imageBytes = ImageReceivedQueue.removefromq()
        image = Image.open(io.BytesIO(imageBytes))
        image.show()
        server_img_name = "server_"+str(server_img_counter) + ".jpg"
        image_save_path = dir_server_image_dump+ "/"+ server_img_name
        print("saving image: ",server_img_name)
        
        image.save(image_save_path)
        FaceRecognitionComplete.Run_Face_Recognition(image_save_path)

        server_img_counter = server_img_counter + 1
    
#    image = Image.open(io.BytesIO(buffer))
#    image.show()
#    server_img_name = "server_"+str(server_img_counter) + ".jpg"
#    print("saving image: ",server_img_name)
#    image.save(server_img_name)
#    server_img_counter = server_img_counter + 1
    
    

    print('Done Receiving')
#    conn.sendto(thanks_message.encode(),(host,port))
    conn.close()