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
import _thread
import time
import datetime

ImageFile.LOAD_TRUNCATED_IMAGES = True

port = FaceRecognitionComplete.Server_Port()     # Reserve a port for your service.
deleteTrainImages = FaceRecognitionComplete.Delete_Train_Images()
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

generated_directory = "GeneratedData"
if not os.path.exists(generated_directory):
    os.makedirs(generated_directory)
    
    
dir_server_image_dump = generated_directory + "/Server_Image_Received_Dump"
if not os.path.exists(dir_server_image_dump):
    print("creating server images folder")
    os.makedirs(dir_server_image_dump)


def recvall(sock,addr):
    print("Server is receiving image from ",addr)
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
#        print(Image_Size)
        
    return data

            



def Server_Run_Forever():


    print("############################################")
    print ('Server Ready. Launch the client :)')
    server_img_counter = 0
    
    while True:
        conn_client_socket, addr = s.accept()     # Establish connection with client.
        _thread.start_new_thread(recvall,(conn_client_socket,addr))
        if(ImageReceivedQueue.isEmpty() == False):
            print("new image in the queue")
            imageBytes = ImageReceivedQueue.removefromq()
            image = Image.open(io.BytesIO(imageBytes))
    #        image.show()
            Time_Stamp = time.time()
            Time_Stamp = datetime.datetime.fromtimestamp(Time_Stamp).strftime('%Y-%m-%d_%Hh%Mm%Ss')
            server_img_name = "server_"+str(server_img_counter)+"_"+ str(Time_Stamp) + ".jpg"
            image_save_path = dir_server_image_dump+ "/"+ server_img_name
            print("saving image: ",server_img_name)
            
            image.save(image_save_path)
            
            FaceRecognitionComplete.Run_Face_Recognition(image_save_path)
            
            if deleteTrainImages == 1:
                ## If file exists, delete it ##
                if os.path.isfile(image_save_path):
                    print("Deleting Train Image: ",image_save_path)
                    os.remove(image_save_path)
                else:    ## Show an error ##
                    print("Error: %s file not found" % image_save_path)
                
                
            server_img_counter = server_img_counter + 1
        
#    image = Image.open(io.BytesIO(buffer))
#    image.show()
#    server_img_name = "server_"+str(server_img_counter) + ".jpg"
#    print("saving image: ",server_img_name)
#    image.save(server_img_name)
#    server_img_counter = server_img_counter + 1


##########################################################################################
def main():
    
    if(FaceRecognitionComplete.Train_Again_Face_Images() == 1):
        FaceRecognitionComplete.Generate_Encoding_From_Images()

    FaceRecognitionComplete.Train_On_Encoding_File()
    try:
        print("Running server forever")
        Server_Run_Forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        s.close()
        
        
##########################################################################################
if __name__ == "__main__":
    print("Server Launched")
    main()