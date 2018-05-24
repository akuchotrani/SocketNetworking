# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 17:14:38 2018

@author: aakash.chotrani
"""

import face_recognition
import cv2
import os
import json
import multiprocessing
from multiprocessing import freeze_support
from multiprocessing import Pool

known_face_names = []
known_face_encodings = []
directory_already_trained = []
dir_path = ''
    
with open('ApplicationParameters.json') as json_data:
    Data = json.load(json_data)
    print('Json Application Param Data')
    print(Data)

CameraIndex = Data['CameraIndex']    
CaptureTimer = float(Data['ImageCaptureTimer'])
KnownPersonConfidence =float(Data['KnownPersonConfidence'])
KnownPersonNewFaceConfidence =float(Data['KnownPersonNewFaceConfidence'])
SharedFolderPath = Data['SharedFolderPath']


dir_save_face_path = "//" + SharedFolderPath
if not os.path.exists(dir_save_face_path):
    os.makedirs(dir_save_face_path)
dir_path = dir_save_face_path

    
    



Known_People_Count = 0
def Train_Known_Faces():
    global Known_People_Count
    global directory_already_trained
    directory_already_trained = []

    for entry in os.scandir(dir_path):
        if entry.is_dir():
            Known_People_Count = Known_People_Count + 1
            #keeping track of all the directories already trained
            directory_already_trained.append(entry.path)
            for entry2 in os.scandir(entry.path):
                if entry2.is_file():
                    image = face_recognition.load_image_file(entry2.path)
                    face_encodings = face_recognition.face_encodings(image)
                    if len(face_encodings) == 0:
                        continue
                    
                    face_encoding = face_encodings[0]
                    known_face_names.append(entry.name)
                    known_face_encodings.append(face_encoding)


def Train_Face_Captured_By_Another_Camera(folder_name,path):
    for file in os.scandir(path):
        if file.is_file():
            image = face_recognition.load_image_file(file.path)
            face_encodings = face_recognition.face_encodings(image)
            if len(face_encodings) == 0:
                continue
            face_encoding = face_encodings[0]
            known_face_names.append(folder_name)
            known_face_encodings.append(face_encoding)





def Run_Face_Recognition(currentCameraIndex):
    global directory_already_trained
    print('Running Face recognition for camera index:',currentCameraIndex)
    video_capture = cv2.VideoCapture(currentCameraIndex)
    face_names_found = []
    
    print('Directory already trained:',directory_already_trained)
    print("Folders found:")
    for folder in os.scandir(dir_path):
        if folder.is_dir():
            print(folder.path)
            if (str(folder.path) in directory_already_trained):
                print ("Already trained")
            else:
                print("New Folder Detected")
                Train_Face_Captured_By_Another_Camera(folder.name,folder.path)

    
    while True:
        
        face_names_found.clear()
        
        ret, frame = video_capture.read()
        rgb_frame = frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            
            #matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    
            name = "Unknown"
            
            lowest_distance = 1.0
            lowest_index = 0
            found = False
            
            for i, face_distance in enumerate(distances):
                
                if lowest_distance > face_distance:
                    lowest_distance = face_distance
                    lowest_index = i
                
            if lowest_distance < KnownPersonConfidence:
                    name = known_face_names[lowest_index]
                    found = True
    
            if found == False:
                face_image = frame[top:bottom, left:right]    
                #We know this person but less confident
                if lowest_distance < KnownPersonNewFaceConfidence:
                    name = known_face_names[lowest_index]
                    dir_name = dir_path + "/" + name
                    cv2.imwrite(dir_name + "/" + str(len(known_face_names)) + ".jpg", face_image)
                    known_face_names.append(name)
                    known_face_encodings.append(face_encoding)
                #We have seen this face for the first time. Create a new directory.
                else:
                    name = "face_" + str(len(known_face_names))
                    dir_name = dir_path + "/" + name
                    if not os.path.exists(dir_name):
                        print('making a new directory:',dir_name)
                        os.makedirs(dir_name)
                    cv2.imwrite(dir_name + "/1.jpg", face_image)
                    known_face_names.append(name)
                    known_face_encodings.append(face_encoding)
                    
            face_names_found.append(name)
        
        #Creating another loop to draw rectangles on faces in the frame for debugging purpose.
        index = 0
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, face_names_found[index], (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            index  = index + 1
        
        videoFeedTitle = 'CAM --------->' + str(currentCameraIndex)
        cv2.imshow( videoFeedTitle,frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    
    cv2.destroyAllWindows()

    


def ApplicationMain(camIndex):
    print('Training Known Faces')
    Train_Known_Faces()
    Run_Face_Recognition(camIndex)

if __name__ == '__main__':
#    __spec__ = "ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>)"
    print('------------------Application started-------------------')
    print("Reading Json Data")    
    
    multiprocessing.freeze_support()
    pool = Pool(len(CameraIndex))
    pool.map(ApplicationMain,CameraIndex)
    





