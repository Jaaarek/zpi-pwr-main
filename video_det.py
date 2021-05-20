import cv2
import numpy as np
import face_recognition
import os
import time

KNOWN_FACES_DIR = "cameras_microservice/ImagesAttendance"
TOLARANCE = 0.5
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog" #HOG ALG

video = cv2.VideoCapture('3.avi')
video.set(cv2.CAP_PROP_FPS, 5)

known_faces = []
known_names = []


for filename in os.listdir(f"{KNOWN_FACES_DIR}"):
    image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(filename)



print("processing unknown faces")
while video.isOpened():

    ret, img = video.read()
    locations = face_recognition.face_locations(img, model=MODEL)
    encodings = face_recognition.face_encodings(img, locations)
    #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    for face_encoding, face_location in zip(encodings, locations):
        results = face_recognition.compare_faces(known_faces, face_encoding, TOLARANCE)
        match = None
        if True in results:
            match = known_names[results.index(True)]
            print(f"Match found: {match}")

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0,255,0]
            cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)

            top_left = (face_recognition[3], face_recognition[2])
            bottom_right = (face_recognition[1], face_recognition[2]+22)
            cv2.rectangle(img, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(img, match, (face_recognition[3]+10, face_recognition[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), FONT_THICKNESS)

        else:
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])
            color = [0, 0, 255]
            cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)
            name = 'UNKNOWN'
            cv2.putText(img, name, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), FONT_THICKNESS)
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            cv2.destroyWindow(filename)






#img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
#frame = cv2.imencode('.jpg', img)[1].tobytes()
#yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#time.sleep(0.1)
#else:
#break

