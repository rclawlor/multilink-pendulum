import numpy as np
import cv2
import imutils
from collections import deque
import threading
from time import sleep

directory = "/home/ronan/IIB/4M25/python/tracking_demo/"

RADIUS = 5

c = threading.Condition()
x = 0
y = 0

# Separate thread for image processing and data saving
class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
    
    def run(self):
        global x
        global y
        # Set range of colours to track
        measured = np.array([240,40,40],dtype="uint8")
        redLower = measured-np.array([40,30,30])
        redUpper = measured+np.array([30,30,30])
        # Fixed length trajectory for drawing on image
        trajectory = deque([], maxlen=50)

        n = 1
        while True:
            # Grab frame (this is from saved images, but uses live footage on Raspberry Pi in practice)
            frame = cv2.imread(directory+str(n).zfill(4)+".png")
            # Create binary image where 1's correspond to where the frame is within the defined colour range
            red = cv2.inRange(frame,redLower,redUpper)
            # Blur binary image
            red = cv2.GaussianBlur(red,(3,3),0)
            # Find contours in this
            cnts = cv2.findContours(red.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            # If object found...
            if len(cnts) > 0:
                # Sort contours by area size
                cnt = sorted(cnts,key=cv2.contourArea,reverse=True)[0]
                # Compute rectangle they lie within
                rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))
                # Centre of rectangle is the object centre
                center = (rect[0][0]+(rect[-1][0] - rect[0][0])//2,rect[1][1]+(rect[-1][-1]-rect[1][1])//2)
                trajectory.append(center)
                x = center[0]
                y = center[1]
                cv2.circle(frame, center, 
                    RADIUS, (0, 220, 0), -1)
                for i in range(1, len(trajectory)):
                    if trajectory[i - 1] is None or trajectory[i] is None:
                        continue
                    thickness = 2
                    cv2.line(frame, trajectory[i - 1], trajectory[i], (0, 220, 0), thickness)
            cv2.imshow("BALLS", frame)
            n += 1
            if n==260:
                n = 1
            
            if cv2.waitKey(1)==27:
                break

class Thread_B(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global x
        global y
        while True:
            # c.acquire()
            print(f"{x} {y}")
            # c.notify_all()

if __name__=="__main__":
    x = 0
    y = 0
    a = Thread_A("myThread_name_A")
    b = Thread_B("myThread_name_B")

    b.start()
    a.start()

    a.join()
    b.join()