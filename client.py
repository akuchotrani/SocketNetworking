# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:44:22 2018

@author: aakash.chotrani
"""

import socket                   # Import socket module
import cv2

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

last_image_captured = ""
def Capture_Webcam_Image():
    cam = cv2.VideoCapture(0)
    image_counter = 0
    while True:
        ret,frame = cam.read()
        cv2.imshow("webcam image",frame)
        if not ret:
            break
        
        key = cv2.waitKey(1)
        
        if key%256 == 27:
            print("Escape pressed, closing....")
            break
        elif key%256 == 32:
            #Space pressed
            img_name = host + str(image_counter) + ".jpg"
            cv2.imwrite(img_name, frame)
            image_counter = image_counter + 1


def Send_Image_To_Server():
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
    image_file.close()
    print('Successfully sent the file')
    s.close()
    print('connection closed')
    
    
def main():
    print("Client Code")
    Capture_Webcam_Image() 
    Send_Image_To_Server()


if __name__ == "__main__":
    main()
    

