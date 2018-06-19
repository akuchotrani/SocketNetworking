# -*- coding: utf-8 -*-
"""
Created on Fri May 18 13:44:22 2018
@author: aakash.chotrani
"""

import socket                   # Import socket module
import cv2
import time
import json
import os



generated_directory = "GeneratedData"
if not os.path.exists(generated_directory):
    os.makedirs(generated_directory)

dir_client_image_dump = generated_directory + "/Client_Captured_Images_Dump"
if not os.path.exists(dir_client_image_dump):
    print("creating client images folder")
    os.makedirs(dir_client_image_dump)

with open('ClientParameters.json') as json_data:
    Data = json.load(json_data)
    print('Json Application Param Data')
    print(Data)
    


CAM_Index = int(Data['CameraIndex'])

timer_delay_capture = float(Data['ImageCaptureTimer'])
SERVER_IP = Data['ServerIP']


Frame_Width_Resolution = float(Data['ResolutionWidth'])
Frame_Height_Resolution = float(Data['ResolutionHeight'])

host = socket.gethostname()     # Get local machine name
print("client host name:",host)
port = int(Data['Port'])                    # Reserve a port for your service.

deleteTrainImages = int(Data['DeleteTrainImage'])


CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4


def Capture_Webcam_Image():
#    cam = cv2.VideoCapture(CAM_Index)
#    cam.set(CV_CAP_PROP_FRAME_WIDTH,Frame_Width_Resolution)
#    cam.set(CV_CAP_PROP_FRAME_HEIGHT,Frame_Height_Resolution)
    cam = cv2.VideoCapture('LosAngeles.mp4')
    cam.set(CV_CAP_PROP_FRAME_WIDTH,Frame_Width_Resolution)
    cam.set(CV_CAP_PROP_FRAME_HEIGHT,Frame_Height_Resolution)
    
    
    image_counter = 0
    
    capture_time = time.time() + timer_delay_capture
    while True:
        ret,original_frame = cam.read()
        #remove this line 
        original_frame = cv2.resize(original_frame, (1920, 1080), interpolation = cv2.INTER_LINEAR)

#        cv2.imshow('frame',original_frame)
        frame = original_frame[:, :, ::-1]
        cv2.imshow("webcam image",original_frame)
        if not ret:
            cv2.release()
            cv2.destroyAllWindows()
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
            print("capturing image: ",img_name)
            Send_Image_To_Server(img_name,s)
            s.close()
        
        
        
        #sending images through a timer
        currentTime = time.time()        
        if(currentTime > capture_time):
            s = socket.socket()             # Create a socket object
            s.connect((SERVER_IP , port))
            img_name = host + str(image_counter) + ".jpg"
            image_save_path = dir_client_image_dump+ "/"+ img_name
            cv2.imwrite(image_save_path, frame)
            image_counter = image_counter + 1
            print("capturing image: ",img_name)
            Send_Image_To_Server(image_save_path,s)
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
    if deleteTrainImages == 1:
        ## If file exists, delete it ##
        if os.path.isfile(image_name):
            print("Deleting Client Dump Image: ",image_name)
            os.remove(image_name)
        else:    ## Show an error ##
            print("Error: %s file not found" % image_name)

    
    
def main():
    print("Client Launched")
    Capture_Webcam_Image() 


if __name__ == "__main__":
    main()