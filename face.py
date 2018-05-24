import face_recognition
import cv2
import os
from PIL import Image



#folders = []
#files = []
known_face_names = []
known_face_encodings = []

dir_path = os.path.dirname(os.path.realpath(__file__)) + "/faces"

for entry in os.scandir(dir_path):
    if entry.is_dir():
        for entry2 in os.scandir(entry.path):
            if entry2.is_file():
                image = face_recognition.load_image_file(entry2.path)
                face_encodings = face_recognition.face_encodings(image)
                if len(face_encodings) == 0:
                    continue
                
                face_encoding = face_encodings[0]
                known_face_names.append(entry.name)
                known_face_encodings.append(face_encoding)
        
        


video_capture = cv2.VideoCapture(0)   

#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
     
while True:

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
            
#            if face_distance < 0.3:
#                first_match_index = matches.index(True)
#                name = known_face_names[first_match_index]
#                found = True
#                break
            
        if lowest_distance < 0.4:
                name = known_face_names[lowest_index]
                found = True

        if found == False:
            face_image = frame[top:bottom, left:right]    
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            fm = variance_of_laplacian(gray)
            
            if (fm < 200) :
                continue
            
            if lowest_distance < 0.6:
                name = known_face_names[lowest_index]
                dir_name = dir_path + "/" + name
                cv2.imwrite(dir_name + "/" + str(len(known_face_names)) + ".jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)
            else:
                name = "face_" + str(len(known_face_names))
                dir_name = dir_path + "/" + name
                os.makedirs(dir_name)
                cv2.imwrite(dir_name + "/1.jpg", face_image)
                known_face_names.append(name)
                known_face_encodings.append(face_encoding)


#        if True in matches:
#            first_match_index = matches.index(True)
#            name = known_face_names[first_match_index]
#        else:
#            face_image = frame[top:bottom, left:right]     
#            
#            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
#            fm = variance_of_laplacian(gray)
#            
#            print(fm)
#            
#            if (fm < 200) :
#                continue
#            
#            name = "face_" + str(len(known_face_names))
#            dir_name = dir_path + "/" + name
#            os.makedirs(dir_name)
#            cv2.imwrite(dir_name + "/face.jpg", face_image)
#            known_face_names.append(name)
#            known_face_encodings.append(face_encoding)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
 
# Get a reference to webcam #0 (the default one)
#video_capture = cv2.VideoCapture(0)

## Load a sample picture and learn how to recognize it.
#obama_image = face_recognition.load_image_file("faces/obama/obama.jpg")
#obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#
## Load a second sample picture and learn how to recognize it.
#biden_image = face_recognition.load_image_file("faces/biden/biden.jpg")
#biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
#
## Create arrays of known face encodings and their names
#known_face_encodings = [
#    obama_face_encoding,
#    biden_face_encoding
#]
#known_face_names = [
#    "Barack Obama",
#    "Joe Biden"
#]
#
#while True:
#    # Grab a single frame of video
#    ret, frame = video_capture.read()
#
#    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#    rgb_frame = frame[:, :, ::-1]
#
#    # Find all the faces and face enqcodings in the frame of video
#    face_locations = face_recognition.face_locations(rgb_frame)
#    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
#
#    # Loop through each face in this frame of video
#    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#        # See if the face is a match for the known face(s)
#        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#
#        name = "Unknown"
#
#        # If a match was found in known_face_encodings, just use the first one.
#        if True in matches:
#            first_match_index = matches.index(True)
#            name = known_face_names[first_match_index]
#
#        # Draw a box around the face
#        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
#
#        # Draw a label with a name below the face
#        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
#        font = cv2.FONT_HERSHEY_DUPLEX
#        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
#
#    # Display the resulting image
#    cv2.imshow('Video', frame)
#
#    # Hit 'q' on the keyboard to quit!
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
## Release handle to the webcam
#video_capture.release()
#cv2.destroyAllWindows()