from math import sin, cos
from lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)
t = 0


def homing_init(motors):
    pass
    # query motor positions (report error if u cannot get a reply  (comm error))
    #try:
    #    for motor in motors:
            
        # if not response >> comms error
    
    # move slowly to "home" position  (report error if current.temp is too low or high
    
    # CHECK THAT ROBOT REAACHES HOME STATE 
        # error if motors don't reach 

def init_servos():
    try:
        servo_hip = LX16A(1)
        servo_upper_knee = LX16A(6)
        servo_knee = LX16A(3)
        servo_hip.set_angle_limits(0, 240)
        servo_upper_knee.set_angle_limits(0, 240)
        servo_knee.set_angle_limits(0, 240)
    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()

    return servo_hip, servo_upper_knee, servo_knee


def move_forward(servo_hip, servo_upper_knee, servo_knee):
    servo_hip.move(sin(t) * 60 + 60)
    servo_upper_knee.move(cos(t) * 60 + 60)
    servo_knee.move(sin(t) * 60 + 60)


def move_backwards(servo_hip, servo_upper_knee, servo_knee):
    servo_hip.move(cos(t) * 60 + 60)
    servo_upper_knee.move(sin(t) * 60 + 60)
    servo_knee.move(cos(t) * 60 + 60)

def main():
    try:
        servo_hip, servo_upper_knee, servo_knee = init_servos()
        move_forward(servo_hip, servo_upper_knee, servo_knee)
        move_backwards(servo_hip, servo_upper_knee, servo_knee)
    except ServoTimeoutError as e:
        print("Servo disconnected from device")


if __name__ == "__main__":
    main()