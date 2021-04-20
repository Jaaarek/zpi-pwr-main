import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'C:/Users/mibrz/Desktop/face_rec/ImagesAttendance'
images = []
logins = []

imgList = os.listdir(path)


for i in imgList:
    currentImg = cv2.imread(f'{path}/{i}')
    images.append(currentImg)
    logins.append(os.path.splitext(i)[0])


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeImg = face_recognition.face_encodings(img)[0]
        encodeList.append(encodeImg)

    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding complete')

vid = cv2.VideoCapture(0) #tu zamiast 0 ścieżka do filmu
vid.set(cv2.CAP_PROP_FPS, 30)

while True:
    sucess, img = vid.read()
    imgSize = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgSize = cv2.cvtColor(imgSize, cv2.COLOR_BGR2RGB)

    facesCurrentFrame = face_recognition.face_locations(imgSize)
    encodeCurrentFrame = face_recognition.face_encodings(imgSize, facesCurrentFrame)

    for encodeFace, faceLoc in zip(encodeCurrentFrame, facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDist = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchId = np.argmin(faceDist)

        if matches[matchId]:
            name = logins[matchId]
            y1, x2, y2, x1 = faceLoc
            y1, x2q, y2, x1 = 4*y1, 4*x2, 4*y2, 4*x1
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_ITALIC, 1, (255,255,255), 2)
        else:
            name = "UNKNOWN"
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = 4*y1, 4*x2, 4*y2, 4*x1
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_ITALIC, 1, (0, 0, 255), 2)



    cv2.imshow('img', img)
    if cv2.waitKey(30) & 0xFF == ord('q'): #Wyłącznie kamerki na przycisk q
        break













