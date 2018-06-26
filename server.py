# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:49:43 2018

@author: aakash.chotrani
"""

##########################################################################################

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







Client_Room_Dictionary = {}

def Check_Room_Present_Client(client_socket, client_address):
    
    client_ipv4 = client_address[0]
    
    if client_ipv4 in Client_Room_Dictionary:
        print("Client room name already present: ADDRESS:",client_ipv4,' room_name: ',Client_Room_Dictionary[client_ipv4])
        #returning true since already present hence start receiving image
        return True
    else:
        room_name = client_socket.recv(1024).decode()
        print("Adding client address:",client_ipv4," and room_name:",room_name," to dictionary")
        Client_Room_Dictionary[client_ipv4] = room_name
        #returning false since I just added this string. False indicates that this is a room name bytes not an image bytes.
        return False

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
RoomName_Of_Image_Queue = Queue()
#####################################################################################

generated_directory = "GeneratedData"
if not os.path.exists(generated_directory):
    os.makedirs(generated_directory)
    
    
dir_server_image_dump = generated_directory + "/Server_Image_Received_Dump"
if not os.path.exists(dir_server_image_dump):
    print("creating server images folder")
    os.makedirs(dir_server_image_dump)


##########################################################################################


def recvall(sock,addr):
    
    if(Check_Room_Present_Client(sock,addr) == True):
        print("Server is receiving image from ",addr[0])
        BUFF_SIZE = 4096 # 4 KiB
        Image_Size = 0
        data = b''
        while True:
            part = sock.recv(BUFF_SIZE)
            data += part
            
            if part == b'':
                ImageReceivedQueue.addtoq(data)
                room_name = Client_Room_Dictionary[addr[0]]
                RoomName_Of_Image_Queue.addtoq(room_name)
            
                data = b''
                Image_Size = 0
                break
            
            
            Image_Size += 4096
    #        print(Image_Size)
        
#    return data

            

##########################################################################################


def Server_Run_Forever():


    print("############################################")
    print ('Server Ready. Launch the client :)')
    server_img_counter = 0
    
    while True:
        conn_client_socket, addr = s.accept()     # Establish connection with client.
        _thread.start_new_thread(recvall,(conn_client_socket,addr))
        
        
        if(ImageReceivedQueue.isEmpty() == False):
            imageBytes = ImageReceivedQueue.removefromq()
            roomName = RoomName_Of_Image_Queue.removefromq()
            image = Image.open(io.BytesIO(imageBytes))
    #        image.show()
            Time_Stamp = time.time()
            Time_Stamp = datetime.datetime.fromtimestamp(Time_Stamp).strftime('%Y-%m-%d_%Hh%Mm%Ss')
            server_img_name = "server_"+str(server_img_counter)+"_"+ str(Time_Stamp)+"_"+str(roomName) + ".jpg"
            image_save_path = dir_server_image_dump+ "/"+ server_img_name
            print("saving image: ",server_img_name)
            
            image.save(image_save_path)
            
            FaceRecognitionComplete.Run_Face_Recognition(image_save_path,roomName)
            
            if deleteTrainImages == 1:
                ## If file exists, delete it ##
                if os.path.isfile(image_save_path):
                    print("Deleting Train Image: ",image_save_path)
                    os.remove(image_save_path)
                else:    ## Show an error ##
                    print("Error: %s file not found" % image_save_path)
                
                
            server_img_counter = server_img_counter + 1
        


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