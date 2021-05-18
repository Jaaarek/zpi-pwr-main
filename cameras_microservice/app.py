import cv2
import time
from flask import Response, Flask


app = Flask(__name__)

def gen():
    """Video streaming generator function."""
    cap = cv2.VideoCapture('768x576.avi')

    # Read until video is completed
    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, img = cap.read()
        if ret == True:

            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            time.sleep(0.1)
        else:
            break


@app.route('/video_feed', methods=['GET'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response (gen(), mimetype='multipart/x-mixed-replace; boundary=frame')
#mimetype='multipart/x-mixed-replace; boundary=frame'

if __name__ == '__main__':
    app.run()