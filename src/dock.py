import cv2
from .util import keyboard_shutdown
import math
from .Camera import camera
import time
from .Rover import *

length = 45
breadth = 30

def moveF(rover:Rover, spd):
    rover.moveForward(speed=spd)

def moveB(rover:Rover, spd):
    rover.moveForward(speed=spd)

def moveF_L(rover:Rover, spd, d):
    rover.moveForward_L(speed=spd,d=d)

def moveB_L(rover:Rover, spd, d):
    rover.moveBackward_L(speed=spd,d=d)

def changeDirection(rover:Rover, angle):
    rover.changeYaw(angle=angle,speed=0.02)

def align(rover:Rover, change):
    rover.changeYaw(angle=math.radians(90), speed=0.02)
    moveF_L(rover, spd=2, d=change)
    rover.changeYaw(angle=-math.radians(90), speed=0.02)



def dock(rover:Rover):
    
    label_font = cv2.FONT_HERSHEY_SIMPLEX
    rover.setupAndArm()
    rover.changeVehicleMode('GUIDED')
    rover.changeYaw(angle=math.radians(90), speed=0.1)
    # print('Done!!!!!')
    moveF_L(rover, spd=2, d=2)
    rover.changeYaw(angle=-math.radians(90), speed=0.1)
    print('Done!!!!!')
   
    # while True:
        
    #     dock_x, masked_image = rover.camera.capture()
    #     masked_image = cv2.rotate(masked_image, cv2.ROTATE_180)
    #     #cv2.imshow('OG', src_image)
    #     FrameCenter_X = round(masked_image.shape[1]/2)
    #     FrameCenter_Y = round(masked_image.shape[0]/2)
    #     masked_image = cv2.circle(masked_image, (FrameCenter_X, FrameCenter_Y), radius=10, color=(255, 0, 0), thickness=-1)
    #     drift = (dock_x-FrameCenter_X)
    #     # print('drift', drift)
    #     K=1
        
    #     if dock_x is not 0:
            
    #         if (drift) > 25:
    #             cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
    #             align(rover, (K*drift))

    #         elif (drift) < -25:
    #             cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
    #             align(rover, (-K*drift))

    #         elif -25 < (drift) < 25 :
    #             cv2.putText(masked_image, "Move Forward", (50, 50), label_font, 0.5, (255, 0, 0), 2)
    #             moveF(rover,spd=2)
        
    #     else:
    #         print("Drone not detected")
        
    #     cv2.imshow('masked', masked_image)
    #     cv2.waitKey(1)


if __name__ == '__main__':
    pass