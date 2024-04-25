
from math import sin, cos
from lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 0.1)

# servo 1: top head
# servo 2: right shin
# servo 3: right leg
# servo 4: left leg
# servo 5: left shin
# servo 6: head lifter
# servo 7: right hip
# servo 8: left hip

# head: 1 -> 6
# left leg: 8 -> 4 -> 5 
# right leg: 7 -> 3 -> 2


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
        servo_hip = LX16A(7)
        servo_upper_knee = LX16A(3)
        servo_knee = LX16A(2)

        servo_hip.set_angle_limits(0, 360)
        servo_upper_knee.set_angle_limits(0, 360)
        servo_knee.set_angle_limits(0, 360)

        #servo_hip.set_angle_offset(-10)

    except ServoTimeoutError as e:
        print(f"Servo {e.id_} is not responding. Exiting...")
        quit()

    print("initialized servos..\n")
    return servo_hip, servo_upper_knee, servo_knee


def move_forward_right(servo_hip, servo_upper_knee, servo_knee):
    t = 0
    offsetHip = 240
    offsetUpperKnee = 15
    offsetKnee = 15

    while True: 
        
        #servo_hip.move(sin(t) * 5 + 235)
        servo_hip.move(235)
        print(servo_hip.get_physical_angle())
        #servo_upper_knee.move(0)
        #servo_knee.move(0)
        #servo_upper_knee.move(10)
        #servo_upper_knee.move(sin(t) * offsetUpperKnee + offsetUpperKnee)
        #servo_knee.move(sin(t) * offsetKnee + 15)

        time.sleep(0.05)
        t += 0.05

def move_forward_left(servo_hip, servo_upper_knee, servo_knee):
    t = 0
    offsetHip = 240
    offsetUpperKnee = 15
    offsetKnee = 15

    while True: 
        #servo_hip.move(sin(t) * 5 + 235)
        servo_hip.move(237, relative=True)
        servo_upper_knee.move(0)
        servo_knee.move(0)
        #servo_upper_knee.move(10)
        #servo_upper_knee.move(sin(t) * offsetUpperKnee + offsetUpperKnee)
        #servo_knee.move(sin(t) * offsetKnee + 15)

        time.sleep(0.05)
        t += 0.05


def move_backwards(servo_hip, servo_upper_knee, servo_knee):
    servo_hip.move(cos(t) * 60 + 60)
    servo_upper_knee.move(sin(t) * 60 + 60)
    servo_knee.move(cos(t) * 60 + 60)

def main():
    print("HI")
    try:
        servo_hip, servo_upper_knee, servo_knee = init_servos()
        move_forward_right(servo_hip, servo_upper_knee, servo_knee)
        #move_backwards(servo_hip, servo_upper_knee, servo_knee)
    except ServoTimeoutError as e:
        print("Servo disconnected from device")


if __name__ == "__main__":
    print("executing...")
    main()