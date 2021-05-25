import cv2
import time
from flask import Response, Flask
import cv2
import face_recognition
import os
import datetime as dt


app = Flask(__name__)

camera1='3.avi'

def markAttendace(name):
    with open("Attendance.csv", 'r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = dt.datetime.now()
            dateString= now.strftime('%d/%m/%Y')
            timeString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dateString},{timeString}')

def encoding(DIR_NAME):
    known_faces = []
    known_names = []
    for filename in os.listdir(f"{DIR_NAME}"):
        image = face_recognition.load_image_file(f"{DIR_NAME}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_faces.append(encoding)
        known_names.append(filename)
    return [known_faces,known_names]

def gen(camera):
    KNOWN_FACES_DIR = "ImagesAttendance"
    UNKNOWN_FACES_DIR = "UnknownFaces"
    TOLARANCE = 0.5
    FRAME_THICKNESS = 3
    FONT_THICKNESS = 2
    MODEL = "hog"  # HOG ALG




    while True:

        Encoding_knownFaces = encoding(KNOWN_FACES_DIR)
        known_faces = Encoding_knownFaces[0]
        known_names = Encoding_knownFaces[1]

        Encoding_unknownFaces = encoding(UNKNOWN_FACES_DIR)
        unknown_faces = Encoding_unknownFaces[0]
        unknown_names = Encoding_unknownFaces[1]

        video = cv2.VideoCapture(camera)
        video.set(cv2.CAP_PROP_FPS, 5)
    # Read until video is completed
        while True:
            # Capture frame-by-frame


            ret, img = video.read()
            if ret == True:
                ret, img = video.read()
                locations = face_recognition.face_locations(img, model=MODEL)
                encodings = face_recognition.face_encodings(img, locations)
                # image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

                for face_encoding, face_location in zip(encodings, locations):
                    results = face_recognition.compare_faces(known_faces, face_encoding, TOLARANCE)
                    match = None
                    if True in results:
                        match = known_names[results.index(True)]
                        print(f"Match found: {match}")

                        top_left = (face_location[3], face_location[0])
                        bottom_right = (face_location[1], face_location[2])
                        color = [0, 255, 0]
                        cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)

                        top_left = (face_recognition[3], face_recognition[2])
                        bottom_right = (face_recognition[1], face_recognition[2] + 22)
                        cv2.rectangle(img, top_left, bottom_right, color, cv2.FILLED)
                        cv2.putText(img, match, (face_recognition[3] + 10, face_recognition[2] + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                        markAttendace("elonN")

                    else:
                        results = face_recognition.compare_faces(unknown_faces, face_encoding, TOLARANCE)
                        if False in results:
                            img_counter=len(unknown_faces) + 1
                            img_name = "Unknown_{}.png".format(img_counter)
                            cv2.imwrite(img_name, img)

                        top_left = (face_location[3], face_location[0])
                        bottom_right = (face_location[1], face_location[2])
                        color = [0, 0, 255]
                        cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)
                        name = 'UNKNOWN'
                        cv2.putText(img, name, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                    0.5,
                                    (0, 0, 255), FONT_THICKNESS)
                        markAttendace("elon")




                img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.1)
            else:
                break




@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')
