from flask.wrappers import Request
import requests
import cv2
import time
from flask import Response, Flask, request, render_template, send_from_directory, json, jsonify, flash
import cv2
import face_recognition
import os
import datetime as dt
import shutil


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
    return [known_faces, known_names]

def gen(camera):
    KNOWN_FACES_DIR = "/app/ImagesAttendance"
    UNKNOWN_FACES_DIR = "/app/UnknownFaces"
    TOLARANCE = 0.6
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

                        top_left = (face_location[3], face_location[0])
                        bottom_right = (face_location[1], face_location[2])
                        color = [0, 255, 0]
                        cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)

                        top_left = (face_recognition[3], face_recognition[2])
                        bottom_right = (face_recognition[1], face_recognition[2] + 22)
                        cv2.rectangle(img, top_left, bottom_right, color, cv2.FILLED)
                        cv2.putText(img, match, (face_recognition[3] + 10, face_recognition[2] + 15),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)
                        markAttendace(match)

                else:
                    results = face_recognition.compare_faces(unknown_faces, face_encoding, TOLARANCE)
                    name = None
                    if True not in results or len(unknown_faces) == 0:
                        img_counter = len(unknown_faces) + 1
                        img_name = "Unknown_{}.png".format(img_counter)
                        cv2.imwrite(f"{UNKNOWN_FACES_DIR}/{img_name}", img)
                        enc = face_recognition.face_encodings(img)[0]
                        unknown_faces.append(enc)
                        name = img_name[:-4]
                        unknown_names.append(img_name)


                    if True in results:
                        name = unknown_names[results.index(True)][:-4]

                    top_left = (face_location[3], face_location[0])
                    bottom_right = (face_location[1], face_location[2])
                    color = [0, 0, 255]
                    cv2.rectangle(img, top_left, bottom_right, color, FRAME_THICKNESS)
                    cv2.putText(img, name, (face_location[3] + 10, face_location[2] + 15), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 0, 255), FONT_THICKNESS)
                    markAttendace(name)



                img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                frame = cv2.imencode('.jpg', img)[1].tobytes()
                yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                time.sleep(0.1)
            else:
                break

@app.route('/')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(camera1), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("/app/UnknownFaces", filename)


@app.route('/video_feed1', methods =['GET', 'POST'])
def get_gallery():
    image_names = os.listdir('/app/UnknownFaces')
    print(image_names, flush=True)

    if request.method == 'POST':
        unknown_user = request.form['unknown_user']
        print(unknown_user, flush=True)
        username = request.form['username_add'].lower()
        password = request.form['password_add']
        password2 = request.form['password_add2']
        credential = 'user'
        if credential == 'Użytkownik':
            credential = 'user'
        elif credential == 'Administrator':
            credential = 'admin'
        elif credential == 'Operator':
            credential = 'operator'

        if password != password2:
            flash("Hasła nie są jednakowe")
        else:
            response = requests.post("http://user:12000/new_user", json = {"username": username, "password": password, "credential": credential})
            # if response.json()['status'] == "exist":
            #     flash("Taki użytkownik już istnieje")
            # if response.json()['status'] == "created":
            #     flash("Pomyślnie utworzono użytkownika")
            os.rename(f"/app/UnknownFaces/{unknown_user}", f"/app/UnknownFaces/{username}" )
            shutil.move(f"/app/UnknownFaces/{username}", f"/app/ImagesAttendance{username}" )


    return render_template('camera.html', image_names=image_names)

