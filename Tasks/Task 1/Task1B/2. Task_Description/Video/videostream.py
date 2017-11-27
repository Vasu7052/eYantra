import numpy as np
import cv2
import datetime

print cv2.__version__
cap = cv2.VideoCapture('./Video.mp4')
print cap.isOpened()
print cap.get(cv2.CAP_PROP_FPS)
#cap.set(cv2.CAP_PROP_POS_FRAMES,1)
#cap.grab()
ret, frame = cap.read()
count = 0
start_time = datetime.datetime.now()
while(ret):
    ret2, frame = cap.read()
    print ret2
    if(ret2):
        if(count==100):
            cv2.imwrite("frame.jpg",frame)
            #break
        cv2.imshow('frame',frame)
        cv2.waitKey(40)
        count+=1
    else:
        break
    
print count
cap.release()
#cv2.destroyAllWindows()
end_time = datetime.datetime.now()
tp = end_time-start_time
print tp
