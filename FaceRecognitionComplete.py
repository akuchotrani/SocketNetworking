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

import time
import datetime
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

#CameraIndex = Data['CameraIndex']    
#CaptureTimer = float(Data['ImageCaptureTimer'])

Port = int(Data['Port'])
DeleteTrainImages = int(Data['DeleteTrainImages'])
KnownPersonConfidence =float(Data['KnownPersonConfidence'])
KnownPersonNewFaceConfidence =float(Data['KnownPersonNewFaceConfidence'])
TrainAgainOnFaces = int(Data['TrainAgainOnFaces'])
#SharedFolderPath = Data['SharedFolderPath']


generated_directory = "GeneratedData"
if not os.path.exists(generated_directory):
    os.makedirs(generated_directory)





#dir_save_face_path = "//" + SharedFolderPath
dir_save_face_path = generated_directory + "/Face_Classification"
if not os.path.exists(dir_save_face_path):
    os.makedirs(dir_save_face_path)
dir_path = dir_save_face_path

    
    



Known_People_Count = 0
def Generate_Encoding_From_Images():
    print('#########################################')
    print('Retraining on face images')
    
    
    global Known_People_Count

    print("Removing the previous encoding and known face text files")
    encodingFile_path = Path(generated_directory + '/Encoding.txt')
    if encodingFile_path.exists():
        print("Previous Version Removed: Encoding.txt")
        os.remove(encodingFile_path)
    
    knownNamesFile_Path = Path(generated_directory + '/Known_Names.txt')
    if knownNamesFile_Path.exists():
        print("Previous Version Removed: Known_Names.txt")
        os.remove(knownNamesFile_Path)
    
    print("Scanning the directory for training: ",dir_path)
    print("#### PLEASE WAIT TRAINING... #####")
    for entry in os.scandir(dir_path):
        if entry.is_dir():
            Known_People_Count = Known_People_Count + 1
            #keeping track of all the directories already trained
            for entry2 in os.scandir(entry.path):
                if entry2.is_file():
                    image = face_recognition.load_image_file(entry2.path)
                    face_encodings = face_recognition.face_encodings(image)
                    if len(face_encodings) == 0:
                        continue
                    
                    face_encoding = face_encodings[0]
                    known_face_names.append(entry.name)
                    known_face_encodings.append(face_encoding)
                    Write_Encoding_To_File(face_encoding)

    
    print("Number of known faces trained:",Known_People_Count)


#def Train_Face_Captured_By_Another_Camera(folder_name,path):
#    for file in os.scandir(path):
#        if file.is_file():
#            image = face_recognition.load_image_file(file.path)
#            face_encodings = face_recognition.face_encodings(image)
#            if len(face_encodings) == 0:
#                continue
#            face_encoding = face_encodings[0]
#            known_face_names.append(folder_name)
#            known_face_encodings.append(face_encoding)



def Delete_Train_Images():
    return DeleteTrainImages

def Server_Port():
    return Port


def Train_Again_Face_Images():
    return TrainAgainOnFaces


def Train_On_Encoding_File():
    global known_face_encodings
    global known_face_names
    print("Loading the encodings known already and face names")
    encodingFile_path = Path(generated_directory + 'Encoding.txt')
    if encodingFile_path.exists():
        encodingFile = open(generated_directory + 'Encoding.txt','rb')
        encodingList = pickle.load(encodingFile)
        known_face_encodings = encodingList
        print("#FaceRecognition.py - #Train_Known_Encoding : known_face_encoding:")
        print(known_face_encodings)
    
    knownNamesFile_Path = Path(generated_directory + '/Known_Names.txt')
    if knownNamesFile_Path.exists():
        knownNamesFile = open(generated_directory + '/Known_Names.txt','rb')
        known_face_names = pickle.load(knownNamesFile)
        print("face known: ",known_face_names)
    else:
        print("Known Names File not found: No faces known")
    
    
def Write_Encoding_To_File(encodingsCaptured):
    encodingFile = open(generated_directory + '/Encoding.txt','wb')
#    encodingFile.write("%s\n"%encodingsCaptured)
    pickle.dump(known_face_encodings,encodingFile)
    encodingFile.close()
    
    knownNamesFile = open(generated_directory + '/Known_Names.txt','wb')
#    encodingFile.write("%s\n"%encodingsCaptured)
    pickle.dump(known_face_names,knownNamesFile)
    knownNamesFile.close()




def Run_Face_Recognition(ServerImagePath):

    global directory_already_trained
    print("----------------------------------------------------")
    print('Running Face recognition for image',ServerImagePath )
    print("----------------------------------------------------")


    
    CurrentImage = face_recognition.load_image_file(ServerImagePath)
    face_locations = face_recognition.face_locations(CurrentImage)
    face_encodings = face_recognition.face_encodings(CurrentImage, face_locations)
    
    Time_Stamp = time.time()
    Time_Stamp = datetime.datetime.fromtimestamp(Time_Stamp).strftime('%Y-%m-%d_%Hh-%Mm-%Ss')
    
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
                cv2.imwrite(dir_name + "/" + str(len(known_face_names))+"_"+ str(Time_Stamp) + ".jpg", face_image)
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
                cv2.imwrite(dir_name + "/" + str(len(known_face_names))+"_"+ str(Time_Stamp) + ".jpg", face_image)
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
                cv2.imwrite(dir_name + "/0_"+"_"+ str(Time_Stamp)+".jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
                Write_Encoding_To_File(face_encoding)

        face_names_found.append(name)
    





