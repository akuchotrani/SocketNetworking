# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:44:22 2018
@author: aakash.chotrani
"""

import socket                   # Import socket module
import cv2

host = socket.gethostname()     # Get local machine name
print("client host name:",host)
port = 60000                    # Reserve a port for your service.

SERVER_IP = '10.10.33.58'
SERVER_HOST_NAME = 'dit2578us'
#ip_test = socket.gethostbyname(SERVER_HOST_NAME)
#print('IPTEST:',ip_test)
#s.connect((SERVER_IP , port))
#message = "Hello from client"
#s.sendto(message.encode(),(host,port))

filename = 'meme.jpg'

def Capture_Webcam_Image():
    cam = cv2.VideoCapture(0)
    image_counter = 0
    while True:
        ret,original_frame = cam.read()
        frame = original_frame[:, :, ::-1]
        cv2.imshow("webcam image",original_frame)
        if not ret:
            break
        key = cv2.waitKey(1)
        
        if key%256 == 27:
            print("Escape pressed, closing....")
            cam.release()
            cv2.destroyAllWindows()
            print('connection closed')
            break
        elif key%256 == 32:
            #Space pressed
            s = socket.socket()             # Create a socket object
            s.connect((SERVER_IP , port))

            img_name = host + str(image_counter) + ".jpg"
            cv2.imwrite(img_name, frame)
            image_counter = image_counter + 1
            print("captureing image: ",img_name)
            Send_Image_To_Server(img_name,s)
            s.close()


def Send_Image_To_Server(image_name,socket):
    print("Client: Send_Image_To_Server: ",image_name)
    image_file = open(image_name,'rb')
    image_size = 0;
    while(True):
        data = image_file.read(4096)
        if not data:
            print('data is empty')
            break
        image_size += 4096
        print(image_size)
        socket.send(data)
    image_file.close()
    print('Successfully sent the file')

    
    
def main():
    print("Client Code")
    Capture_Webcam_Image() 


if __name__ == "__main__":
    main()