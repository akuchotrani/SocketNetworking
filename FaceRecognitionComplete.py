# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 17:14:38 2018

@author: aakash.chotrani
"""

import face_recognition
import cv2
import os
import json
import pickle
from pathlib import Path
#import multiprocessing
#from multiprocessing import freeze_support
#from multiprocessing import Pool

known_face_names = []
known_face_encodings = []
directory_already_trained = []
dir_path = ''

face_names_found = []
face_names_found.clear()
    
with open('ApplicationParameters.json') as json_data:
    Data = json.load(json_data)
    print('Json Application Param Data')
    print(Data)

CameraIndex = Data['CameraIndex']    
CaptureTimer = float(Data['ImageCaptureTimer'])
KnownPersonConfidence =float(Data['KnownPersonConfidence'])
KnownPersonNewFaceConfidence =float(Data['KnownPersonNewFaceConfidence'])
SharedFolderPath = Data['SharedFolderPath']


#dir_save_face_path = "//" + SharedFolderPath
dir_save_face_path = SharedFolderPath
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



def Train_Known_Encodings():
    global known_face_encodings
    global known_face_names
    print("Loading the encodings known already and face names")
    encodingFile_path = Path('Encoding.txt')
    if encodingFile_path.exists():
        encodingFile = open('Encoding.txt','rb')
        encodingList = pickle.load(encodingFile)
        known_face_encodings = encodingList
        print("#FaceRecognition.py - #Train_Known_Encoding : known_face_encoding:")
        print(known_face_encodings)
    
    knownNamesFile_Path = Path('Known_Names.txt')
    if knownNamesFile_Path.exists():
        knownNamesFile = open('Known_Names.txt','rb')
        known_face_names = pickle.load(knownNamesFile)
        print(known_face_names)
    else:
        print("Known Names File not found: No faces known")
    
    
def Write_Encoding_To_File(encodingsCaptured):
    encodingFile = open('Encoding.txt','wb')
#    encodingFile.write("%s\n"%encodingsCaptured)
    pickle.dump(known_face_encodings,encodingFile)
    encodingFile.close()
    
    knownNamesFile = open('Known_Names.txt','wb')
#    encodingFile.write("%s\n"%encodingsCaptured)
    pickle.dump(known_face_names,knownNamesFile)
    knownNamesFile.close()




def Run_Face_Recognition(ServerImagePath):

    print(known_face_names)
    global directory_already_trained
    print('Running Face recognition for image',ServerImagePath )

    
    CurrentImage = face_recognition.load_image_file(ServerImagePath)
    face_locations = face_recognition.face_locations(CurrentImage)
    face_encodings = face_recognition.face_encodings(CurrentImage, face_locations)
    
    
    
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
                print("I know this person. Capture and Classify to the correct folder")
                face_image = CurrentImage[top:bottom, left:right]    
                name = known_face_names[lowest_index]
                dir_name = dir_path + "/" + name
                if not os.path.exists(dir_name):
                    print('making a new directory:',dir_name)
                    os.makedirs(dir_name)
                cv2.imwrite(dir_name + "/" + str(len(known_face_names)) + ".jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
                Write_Encoding_To_File(face_encoding)
                found = True

        if found == False:
            face_image = CurrentImage[top:bottom, left:right]    
            #We know this person but less confident
            if lowest_distance < KnownPersonNewFaceConfidence:
                print("New Expression of known person. Hence capturing it")
                name = known_face_names[lowest_index]
                dir_name = dir_path + "/" + name
                if not os.path.exists(dir_name):
                    print('making a new directory:',dir_name)
                    os.makedirs(dir_name)
                cv2.imwrite(dir_name + "/" + str(len(known_face_names)) + ".jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
                Write_Encoding_To_File(face_encoding)

            #We have seen this face for the first time. Create a new directory.
            else:
                print("I don't know this person hence creating a new directory")
                name = "face_" + str(len(known_face_names))
                dir_name = dir_path + "/" + name
                if not os.path.exists(dir_name):
                    print('making a new directory:',dir_name)
                    os.makedirs(dir_name)
                cv2.imwrite(dir_name + "/1.jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
                Write_Encoding_To_File(face_encoding)

        face_names_found.append(name)
    





