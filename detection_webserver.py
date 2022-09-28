from flask import Flask, render_template, Response
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os
from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

p=TonalBuzzer(21) 

class VideoStream:
    """Camera object that controls video streaming from the Picamera"""
    def __init__(self,resolution=(640,480),framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3,resolution[0])
        ret = self.stream.set(4,resolution[1])
            
        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

	# Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
	# Start the thread that reads frames from the video stream
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
	# Return the most recent frame
        return self.frame

    def stop(self):
	# Indicate that the camera and thread should be stopped
        self.stopped = True




def detect_and_predict_mask(frame, network, maskNet):
    # grab the dimensions of the frame and then construct a blob
    # from it
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    network.setInput(blob)
    detections = network.forward()

    # initialize our list of faces, their corresponding locations,
    # and the list of predictions from our face mask network
    faces = []
    locs = []
    preds = []

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > 0.7:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = preprocess_input(face)
            face = np.expand_dims(face,axis=0)
            preds = maskNet.predict(face)

            # add the face and bounding boxes to their respective
            # list
            locs.append((startX, startY, endX, endY))

    # only make a predictions if at least one face was detect
    # return a 2-tuple of the face locations and their corresponding
    # locations
    return (locs, preds)

frame_rate_calc = 1
freq = cv2.getTickFrequency()


@app.route('/')
def index():
    """Video streaming home page."""
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
            'title':'Image Streaming',
            'time': timeString
            }
    return render_template('index2.html', **templateData)




def gen_frames():
    global frame_rate_calc
    
    network = cv2.dnn.readNetFromCaffe('deploy.prototxt.txt','res10_300x300_ssd_iter_140000.caffemodel')
    maskNet = load_model('helmet1.h5')
    vs = VideoStream(src=0).start()

    # loop over the frames from the video stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        t1 = cv2.getTickCount()
        
        ret, frame = vs.read()
        frame = imutils.resize(frame, width=500)

        # detect faces in the frame and determine if they are wearing a
        # face mask or not
        (locs, preds) = detect_and_predict_mask(frame,network, maskNet)

        # loop over the detected face locations and their corresponding
        # locations
        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            mask = pred
            print(pred)
            print(mask)

            if mask > 0.7 :
                label = "helmet"
                color = (0,255,0)
                p.stop()
            else :
                label ="No helmet"
                color = (0,0,255)
                p.play(Tone(220.0))
                time.sleep(0.5)
                p.stop()

            # include the probability in the label
            label = "{}: {}".format(label, mask)
            
            labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2) # Get font size
            label_ymin = max(endY, labelSize[1] + 10) # Make sure not to draw label too close to top of window
            
            # display the label and bounding box rectangle on the output
            # frame
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            cv2.rectangle(frame, (startX, label_ymin-labelSize[1]-10), (endX+labelSize[0], label_ymin+baseLine-10), color, cv2.FILLED)
            
            cv2.putText(frame, label, (startX, label_ymin-7),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
           

        # show the output frame
        cv2.imshow("Face Mask Detector", frame)
        key = cv2.waitKey(1) & 0xFF
        
        cv2.putText(frame,'FPS: {0:.2f}'.format(frame_rate_calc),(30,50),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0),2,cv2.LINE_AA)
        
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc= 1/time1
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
            
        ret, buffer = cv2.imencode('.jpg', frame)
        image = buffer.tobytes()
        yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.0.15',port="8080")