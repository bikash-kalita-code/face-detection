import numpy as np
import cv2

cam_id = 2

cap0 = cv2.VideoCapture(cam_id)
#cap1 = cv2.VideoCapture(2)

while True:
    ret0, frame0 = cap0.read()
    #ret1, frame1 = cap1.read()

    if(ret0):
        cv2.imshow(str(cam_id), frame0)

    #if (ret1):
    #    cv2.imshow('Cam 1', frame1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap0.release()
#cap1.release()
cv2.destroyAllWindows()

# 0r,2l
