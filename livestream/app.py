#  we would want to be able to watch the live stream of the video anyplace and anytime you like.

# Most of the people use IP cameras, it's type of digital video camera that receives control data and sends image data via an IP network. 

# No need local recording device.

# Most IP cameras are RTSP ( Real Time Streaming Protocol ) based


from flask import Flask, render_template, Response
import cv2


#Initialize the Flask app
app = Flask(__name__)


camera = cv2.VideoCapture(0) 
# 'rtsp://freja.hiof.no:1935/rtplive/_definst_/hessdalen03.stream'
# for camera : we need to use 

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


