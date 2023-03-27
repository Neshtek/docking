import cv2
import math
from time import sleep
from .Rover import Rover

def align(rover:Rover, turn, drift):
    print('Changing Yaw')
    sleep(1)
    rover.change_yaw(angle=math.radians(turn * 90), speed=0)
    print('Yaw changed')
    sleep(1)
    print('moving forward')
    rover.move_forward_dist(speed=0.05, dist=0.1)
    sleep(1)
    print('anti-clockwise')
    rover.change_yaw(angle=math.radians(turn * (-90)), speed=0)
    sleep(1)
    
def dock(rover:Rover):
    label_font = cv2.FONT_HERSHEY_SIMPLEX
    rover.setup_arm()
    rover.change_vehicle_mode('GUIDED')
    #return
    drift_counter = {
        'L': 0,
        'R': 0,
        'F': 0
        }
   
    while True:
        dock_x, masked_image = rover.camera.capture()
        #cv2.imshow('OG', src_image)
        frame_center_x = round(masked_image.shape[1] / 2)
        frame_center_y = round(masked_image.shape[0] / 2)
        masked_image = cv2.circle(masked_image, (frame_center_x, frame_center_y), radius=10, color=(255, 0, 0), thickness=-1)
        drift = dock_x - frame_center_x
        # print('drift', drift)
        K = 1
        
        if dock_x is not 0:
            if drift < -50:
                cv2.putText(masked_image, "Move Left", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                drift_counter['L'] = drift_counter['L'] + 1
                if drift_counter['L'] > 5:
                    drift_counter['L'] = 0
                    align(rover, -1, (-K * drift))

            elif drift > 50:
                cv2.putText(masked_image, "Move Right", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                drift_counter['R'] = drift_counter['R'] + 1
                if drift_counter['R'] > 5:
                    drift_counter['R'] = 0
                    align(rover, 1, (K * drift))

            elif -50 < drift < 50 :
                cv2.putText(masked_image, "Move Forward", (50, 50), label_font, 0.5, (255, 0, 0), 2)
                drift_counter['F'] = drift_counter['F'] + 1
                if drift_counter['F'] > 5:
                    drift_counter['F'] = 0
                    # rover.move_forward(speed=2)
                    rover.change_vehicle_mode('HOLD')
        
        else:
            print("Drone not detected")
        
        cv2.imshow('masked', masked_image)
        cv2.waitKey(1)

if __name__ == '__main__':
    pass