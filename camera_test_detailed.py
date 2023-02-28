import numpy as np
import cv2

cam_id = 2

cap = cv2.VideoCapture(cam_id)
cap.set(cv2.CAP_PROP_FPS, 4)

while True:
    ret, frame = cap.read()

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    # Frame drop works and has been tested
    #cap.set(cv2.CAP_PROP_FPS, 4)

    if(ret):
        cv2.imshow(str(cam_id), frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# 0r,2l
