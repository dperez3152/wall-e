
from math import sin, cos
from lx16a import *
import time
from enum import Enum

LX16A.initialize("/dev/ttyUSB0", 1)

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

class WalleD:

    def __init__(self):
    # initialize motors
        try:
            # head
            self.head = LX16A(1)
            self.neck = LX16A(6)
            print("hi from __init__\n")
            print(self.head.get_physical_angle())

            # left leg
            self.lhip = LX16A(7)
            self.lleg = LX16A(3)
            self.lknee = LX16A(2)

            # right leg
            self.rhip = LX16A(8)
            self.rleg = LX16A(4)
            self.rknee = LX16A(5)

        except ServoTimeoutError as e:
            print(f"Servo {e.id_} is not responding. Exiting...")
            quit()
        
        self.servos = self.create_servo_dict()
        print("hi from init again")
        print(self.servos['neck'].get_id())
        print(self.servos['neck'].get_physical_angle())
        self.set_servo_angle_limits()

        print("initialized servos..\n")


    def create_servo_dict(self):
        servo_names = ['neck', 'head',
                       'l_hip', 'l_leg', 'l_knee',
                       'r_hip', 'r_leg', 'r_knee']
        servo_values = [self.neck, self.head,
                        self.lhip, self.lleg, self.lknee,
                        self.rhip, self.rleg, self.rknee]
        servos = dict(zip(servo_names, servo_values))

        print("hi from create_servo_dict")
        print(servos['neck'].get_id())
        print(servos['neck'].get_physical_angle())
        return servos

    
    def set_servo_angle_limits(self) -> None:
        for servo in self.servos.values():
            servo.set_angle_limits(0, 240)


    def query_motor_position(self, servo) -> None:
        print("hi from query_motor_pos")
        print(servo.get_id())
        try:
            print(servo.get_physical_angle())
        except ServoTimeoutError as e:
            print(f"[COMMS] Servo {e.id_} is not responding. Exiting...")
            quit()


    def query_motor_temp(self, servo) -> None:
        temp_limit = 75

        if servo.get_temp() > temp_limit:
            raise ServoError(f"[TEMP] Servo {e.id_} is overheating. Exiting...")
            quit()

        
    def query_motor_voltage(self, servo) -> None:
        lower_limit = 6500  # 6.5V
        upper_limit = 7500  # 7.5V

        if servo.get_vin() < lower_limit or servo.get_vin() > upper_limit:
            raise ServoError(f"[VOLT] Servo {e.id_} voltage is outside safe limits. Exiting...")
            quit()
 

    def set_temp_voltage_limits(self) -> None:
        # PROB WON'T NEED
        # LEDs will flash if temp/voltage limits are exceeded
        for servo in self.servos.values():
            servo.set_led_error_triggers(over_temperature= True, over_voltage= True) 
            servo.set_temp_limit(60)
            servo.set_vin_limits(lower_limit = 6.5, upper_limit= 7.5)

    
    def flash_sequence(self, servos: dict):
        # flash all servos in servos 3 times
        
        t = 0
        
        while t < 3:
            for servo in servos.values():
                servo.led_power_on()
            
            time.sleep(0.3)

            for servo in servos.values():
                servo.led_power_off()

            time.sleep(0.3)

            t+=1

    
    def heartbeat(self):
        # flash hip LEDs in a heartbeat
        t = 0
        
        while t < 2:
            self.servos['l_hip'].led_power_on()
            self.servos['r_hip'].led_power_on()
            time.sleep(0.3)

            self.servos['l_hip'].led_power_off()
            self.servos['r_hip'].led_power_off()
            time.sleep(0.3)

            t+=1


    #def move_to_pos(position: Enum["stand", "crouch"]): figure out how to do this
    def move_to_pos(self, position):
        if position == "stand":
            self.servos['l_hip'].move(120)
            self.servos['r_hip'].move(120)
            
            self.servos['l_leg'].move(180)
            self.servos['r_leg'].move(0)
            
            self.servos['l_knee'].move(120)
            self.servos['r_knee'].move[120]

        elif position == "crouch":
            self.servos['l_hip'].move(120)
            self.servos['r_hip'].move(120)
            
            self.servos['l_leg'].move(180)
            self.servos['r_leg'].move(0)
            
            self.servos['l_knee'].move(120)
            self.servos['r_knee'].move[120]

        # ENSURE TARGET POS REACHED

    
    def boot(self):
        for key, servo in self.servos.items():
            print(key)
            print(servo.get_id())
            print(self.servos['l_hip'].get_physical_angle())
            #print(servo.get_physical_angle())
            #self.query_motor_position(servo)
            # enable/disable motors? ensure connected to power
            #self.query_motor_voltage(servo)
            #self.flash_sequence({'head': self.head, 'neck': self.neck})
            #self.flash_sequence({'l_hip': self.lhip, 'l_leg': self.lleg, 'l_knee': self.lknee})
            #self.flash_sequence({'r_hip': self.rhip, 'r_leg': self.rleg, 'r_knee': self.rknee})


    def homing(self):
        # servo 1: top head
        # servo 2: right shin   120
        # servo 3: right leg    180
        # servo 4: left leg     0
        # servo 5: left shin    120
        # servo 6: head lifter
        # servo 7: right hip    120     
        # servo 8: left hip     120                 

        # query motor positions (report error if u cannot get a reply  (comm error))
        #try:
        #    for motor in motors:
                
            # if not response >> comms error
        
        # move slowly to "home" position  (report error if current.temp is too low or high
        
        # CHECK THAT ROBOT REAACHES HOME STATE 
            # error if motors don't reach 

        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.move_to_pos("stand")


    def health_check(self):
        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.query_motor_temp(servo)
            self.query_motor_voltage(servo)

        self.heartbeat()


    def shutdown(self):
        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.move_to_pos("crouch")
            #disable motors?


    def init_servos():
        # NOT TO BE USED, lol
        try:
            # head
            servo_head = LX16A(1)
            servo_neck = LX16A(6)

            servo_head.set_angle_limits(0, 240)
            servo_neck.set_angle_limits(0, 240)

            # left leg
            servo_lhip = LX16A(7)
            servo_lleg = LX16A(3)
            servo_lknee = LX16A(2)

            servo_lhip.set_angle_limits(0, 240)
            servo_lleg.set_angle_limits(0, 240)
            servo_lknee.set_angle_limits(0, 240)

            # right leg
            servo_rhip = LX16A(8)
            servo_rleg = LX16A(4)
            servo_rknee = LX16A(5)

            servo_rhip.set_angle_limits(0, 240)
            servo_rleg.set_angle_limits(0, 240)
            servo_rknee.set_angle_limits(0, 240)

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

            if t%1 == 0 :
                health_check()
            
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
    print("HI WALL-E")
    walle = WalleD()
    walle.boot()
        #try:
        #    servo_hip, servo_upper_knee, servo_knee = init_servos()
        #    move_forward_right(servo_hip, servo_upper_knee, servo_knee)
            #move_backwards(servo_hip, servo_upper_knee, servo_knee)
        #except ServoTimeoutError as e:
        #    print("Servo disconnected from device")


if __name__ == "__main__":
    print("executing...")
    main()