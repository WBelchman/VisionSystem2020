from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2

from table import Table
from GripPipes import BallPipe, PsPipe


class ballDetect():
    min_radius = 40

    def __init__(self):
        self.pipeline = BallPipe()
        self.nt_table = Table(0) #0 for ball table

    def thresh(self, frame):
        self.pipeline.process(frame)
        return self.pipeline.hsv_threshold_output

    def find_ball(self, contours):
        if len(contours) is 0: return [0] * 3

        max_rad = 0
        for cnt in contours:
            (x, y), radius = cv2.minEnclosingCircle(cnt)
            
            if radius > max_rad:
                max_rad = radius
                output = [x, y, radius]
                
        return [int(val) for val in output]

    def update_table(self, output):
        if output[2] > self.min_radius:
            self.nt_table.updateNumber(output[0:1], key=0) #midpoint
            self.nt_table.updateNumber(output[2], key=1) #radius

        else:
            self.nt_table.updateNumber("B", key=0) #Ball not found values
            self.nt_table.updateNumber("B", key=1)
            

class psDetect():

    def __init__(self):
        self.pipeline = PsPipe()
        self.nt_table = Table(1) #1 for PowerStation

    def thresh(self, frame):
        self.pipeline.process(frame)
        return self.pipeline.output

    def find_ps(self, contours):
        if len(contours) is 0: return [0] * 3

        for cnt in [contours[0]]:
            epsilon = 0.1 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)


#Gets team color from networktables
color_table = Table(2)
team_color = color_table.getValue('team_color', None)

while team_color is None:
    team_color = color_table.getValue('team_color', None)


cam = PiCamera()
cam.resolution = (640, 480)
cam.framerate = 32
rawCap = PiRGBArray(cam, size=(640, 480))

ball_detect = ballDetect()
ps_detect = psDetect(team_color)

for frame in cam.capture_continuous(rawCap, format='bgr', use_video_port=True):

    frame = frame.array

    filtered1 = ball_detect.thresh(frame)
    #filtered2 = ps_detect.thresh(frame)
    
    _, thresh1 = cv2.threshold(filtered1, 127, 255, cv2.THRESH_BINARY)
    #_, thresh2 = cv2.threshold(filtered2, 127, 255, cv2.THRESH_BINARY)
    _, contours1, _ = cv2.findContours(thresh1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #_, contours2, _ = cv2.findContours(thresh2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    output1 = ball_detect.find_ball(contours1)
    #output2 = ps_detect.find_ps(contours2)

    ball_detect.update_table(output1)
    #ps_detect.update_table(output2)
            
    rawCap.truncate(0)