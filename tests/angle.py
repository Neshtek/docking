from pymavlink import mavutil
import math

def change_yaw(angle, speed=0):
    vehicle = mavutil.mavlink_connection('127.0.0.1:14550')
    vehicle.wait_heartbeat()
    print("Heartbeat from system (system %u component %u)" % (vehicle.target_system, vehicle.target_component))
    
    print('Arming...')
    vehicle.mav.command_long_send(vehicle.target_system, vehicle.target_component,
                        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

    vehicle.mav.command_long_encode(
	0, 0,
	mavutil.mavlink.MAV_CMD_DO_SET_REVERSE,
	0,
	1,
	0,
	0,
	0,
	0,0, 0)

    vehicle.mav.command_long_encode(
	0, 0,
	mavutil.mavlink.MAV_CMD_REQUEST_MESSAGE,
	0,
	30,
	0,
	0,
	0,
	0,0, 0)
    
    mode = 'GUIDED'
    print("Changing vehicle mode to", mode)
    # Get mode ID
    mode_id = vehicle.mode_mapping()[mode]
    # Set new mode

    vehicle.mav.set_mode_send(
    vehicle.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id)
    msg = vehicle.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)


    print(angle) # Correct angle by adding abs difference in 180 degrees
    system = vehicle.recv_match(type='ATTITUDE', blocking=True)
    initial = math.degrees(system.yaw)
    final = initial + math.degrees(angle)
    current = initial
    # self.vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, self.vehicle.target_system,
    #                 self.vehicle.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED , int(0b100111100111), 0, 0, 0, (speed), 0, 0, 0, 0, 0, angle, 0))
        
    while True:
        vehicle.mav.send(mavutil.mavlink.MAVLink_set_position_target_local_ned_message(10, vehicle.target_system,
                    vehicle.target_component, mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED , int(0b100111100111), 0, 0, 0, (speed), 0, 0, 0, 0, 0, angle, 0))
            
        system = vehicle.recv_match(type='ATTITUDE', blocking=True)
        current = math.degrees(system.yaw)
            
        if final > 180:
            if current > 0:
                change = current - initial
                final_change = change
            else: 
                neg_change = 180 + current
                final_change = change + neg_change
        elif final < -180:
            if current < 0:
                change = initial - current
                final_change = change
            else:
                neg_change = 180 - current
                final_change = change + neg_change
        else:
            final_change = abs(current - initial)
            
        if final_change >= math.degrees(angle):
            return
            
        print('initial head', initial)
        print('current head', current)
        print('change head', final_change)
            
if __name__ == '__main__':
    change_yaw(angle=math.radians(90), speed=0.1)