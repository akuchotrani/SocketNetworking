# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:44:22 2018
@author: aakash.chotrani
"""

import socket                   # Import socket module
import cv2
import time
import json

with open('ClientParameters.json') as json_data:
    Data = json.load(json_data)
    print('Json Application Param Data')
    print(Data)
    


CAM_Index = int(Data['CameraIndex'])

timer_delay_capture = float(Data['ImageCaptureTimer'])
SERVER_IP = Data['ServerIP']
SERVER_HOST_NAME = Data['ServerHostName']


Frame_Width_Resolution = float(Data['ResolutionWidth'])
Frame_Height_Resolution = float(Data['ResolutionHeight'])

host = socket.gethostname()     # Get local machine name
print("client host name:",host)
port = 60000                    # Reserve a port for your service.


CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4


def Capture_Webcam_Image():
    cam = cv2.VideoCapture(CAM_Index)
    cam.set(CV_CAP_PROP_FRAME_WIDTH,Frame_Width_Resolution);
    cam.set(CV_CAP_PROP_FRAME_HEIGHT,Frame_Height_Resolution);
    image_counter = 0
    
    capture_time = time.time() + timer_delay_capture
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
        
        
        
        #sending images through a timer
        currentTime = time.time()        
        if(currentTime > capture_time):
            s = socket.socket()             # Create a socket object
            s.connect((SERVER_IP , port))
            img_name = host + str(image_counter) + ".jpg"
            cv2.imwrite(img_name, frame)
            image_counter = image_counter + 1
            print("captureing image: ",img_name)
            Send_Image_To_Server(img_name,s)
            s.close()
            capture_time = currentTime + timer_delay_capture
            
        


def Send_Image_To_Server(image_name,socket):
    print("Client: Send_Image_To_Server: ",image_name)
    image_file = open(image_name,'rb')
    image_size = 0;
    while(True):
        data = image_file.read(4096)
        if not data:
            break
        image_size += 4096
#        print(image_size)
        socket.send(data)
    image_file.close()
    print('Successfully sent the file')

    
    
def main():
    print("Client Launched")
    Capture_Webcam_Image() 


if __name__ == "__main__":
    main()