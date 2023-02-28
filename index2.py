import cv2
import time
import threading
from threading import *
from websocket import create_connection
import json
import base64
 
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 
# NOTE: As per the below changes, scale_percent hasn't been used and instead image resolution has been defined inside cap.set
def run(cam_id, delayTime, isDisplay, scale_percent):
    cap = cv2.VideoCapture(cam_id)
    #cap.set(cv2.cv2.CV_CAP_PROP_FPS, 4)
    #cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')) # depends on fourcc available camera
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    #cap.set(cv2.CAP_PROP_FPS, 4)
    while cap.isOpened():
        print("Inside while loop of camera id : ", cam_id)
        #time.sleep(0.5)
        ret, frame = cap.read()
        #_, frame = cap.read()
 
        # Original Dimensions
        #print("Original Dimensions Camera ", camera_id, frame.shape)
 
        # Resizing images
        # scale_percent = 50 # percent of original size
        #width = int(frame.shape[1] *  scale_percent / 100)
        #height = int(frame.shape[0] * scale_percent /100)
        #dim = (width, height)
 
        #frame = cv2.resize(frame, dim, interpolation= cv2.INTER_AREA)
 
        # Resized Dimensions
        # print("Resized Dimensions Camera ", camera_id, frame.shape)
        # print("Resized Dimensions Camera : ", cam_id, frame.shape)
 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
 
        # Display the output
        if isDisplay:
            cv2.imshow(str(cam_id), frame)
 
        # for (x, y, w, h) in faces:
            #cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 3)
 
        if len(faces) >= 1:
            for i in range(len(faces)):
                try:
                    (x, y, w, h) = faces[i]
                    cropped_image = frame[y:y+h, x:x+w]
                    res, frame = cv2.imencode('.jpg', cropped_image)
                    data = base64.b64encode(frame).decode('utf-8')
                    data = {"image":data, "cam":cam_id, "timestamp": time.time()}
                    ws.send(json.dumps(data))
                    print("sent from camera : ", cam_id)
                    #time.sleep(0.25)
                except Exception as e:
                    pass
                # cv2.imshow(str(i), cropped_image)
                # cv2.waitKey(333)
            # print("Number of faces in Camera ", camera_id, len(faces))
            # res, frame = cv2.imencode('.jpg', frame)    # from image to binary buffer
            # data = base64.b64encode(frame).decode('utf-8')  # convert to base64 format
            # data = {"image":data, "cam":camera_id}
            # ws.send(json.dumps(data))
            # print(ws.recv())
 
 
        if cv2.waitKey(delayTime) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
 
print("Before Connection")
ws = create_connection('ws://192.168.29.41:4000/websocket_service/')
print(ws)
print("After connection")
 
 
def thread_receive(ws):
    while True:
        print(ws.recv())
t1 = threading.Thread(target=thread_receive, args=(ws,))
t1.start()
 
t2 = threading.Thread(target=run, args=(0, 1000, False, 40))
t3 = threading.Thread(target=run, args=(2, 1000, False, 40))
 
t2.start()
t3.start()
#run(4, 250, False, 50)
