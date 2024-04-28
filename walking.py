
from math import sin, cos, pi
from lx16a import *
import time
from enum import Enum

LX16A.initialize("/dev/ttyUSB0", 1)

# VISUALIZATION OF MOTOR CONFIGURATION: 
# head: 1 -> 6
# left leg: 8 -> 4 -> 5 
# right leg: 7 -> 3 -> 2

class Walle:

    def __init__(self):
    # initialize motors
        try:
            # head
            self.head = LX16A(1)
            self.neck = LX16A(6)

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

        #TODO self.set_servo_angle_limits() why doesn't this work dawg

        print("initialized servos..\n")


    def create_servo_dict(self):
        # create an iterable dict of servos to use for routine functions (boot, health_check, queries, shutdown)
        servo_names = ['neck', 'head',
                       'l_hip', 'l_leg', 'l_knee',
                       'r_hip', 'r_leg', 'r_knee']
        servo_values = [self.neck, self.head,
                        self.lhip, self.lleg, self.lknee,
                        self.rhip, self.rleg, self.rknee]
        servos = dict(zip(servo_names, servo_values))

        return servos

    
    def set_servo_angle_limits(self) -> None:
        # set all servo angle limits to 0-240 (for now, TODO refine maybe)
        # this is a physical limitation of their "servo mode"
        for servo in self.servos.values():
            servo.set_angle_limits(0, 240)


    def query_motor_position(self, servo) -> None:
        # ensure that you can reach each motor and access their current positions
        try:
            servo.get_physical_angle()
            print(servo.get_id(), servo.get_physical_angle())
        except ServoTimeoutError as e:
            print(f"[COMMS] Servo {e.id_} is not responding. Exiting...")
            quit()


    def query_motor_temp(self, servo) -> None:
        # ensure motos temps are below temp_limit
        temp_limit = 75

        if servo.get_temp() > temp_limit:
            raise ServoError(f"[TEMP] Servo {servo.get_id()} is overheating. Exiting...")
            quit()

        
    def query_motor_voltage(self, servo) -> None:
        # ensure motor voltages are within acceptable limits (lower_limit-upper_limit)
        lower_limit = 6500  # 6.5V
        upper_limit = 7500  # 7.5V

        if servo.get_vin() < lower_limit or servo.get_vin() > upper_limit:
            raise ServoError(f"[VOLT] Servo {servo.get_id()} voltage is outside safe limits. Exiting...")
            quit()

    
    def flash_thrice(self, servos_to_flash: dict):
        # TODO consider a better way to pass in the servos you want to flash
        # flash all LEDs in servos 3 times
        flash_duration = 0.3
        for t in range(3):
            for servo in servos_to_flash.values():
                servo.led_power_on()
            time.sleep(flash_duration)

            for servo in servos_to_flash.values():
                servo.led_power_off()
            time.sleep(flash_duration)

    
    def heartbeat(self):
        # flash hip LEDs in a heartbeat
        for t in range(2):
            self.servos['l_hip'].led_power_on()
            self.servos['r_hip'].led_power_on()
            time.sleep(0.3)

            self.servos['l_hip'].led_power_off()
            self.servos['r_hip'].led_power_off()
            time.sleep(0.3)


    # TODO: def move_to_pos(position: Enum["stand", "crouch"]): figure out how to do this
    def move_to_pos(self, desired_position):
        # move wall-e to his home "stand" position or rest "crouch" position
        servos =        ['l_hip', 'r_hip', 'l_leg', 'r_leg', 'l_knee', 'r_knee']
        stand_angles =  [105,      150,     175,    5,       120,       120]
        crouch_angles = [110,      145,     150,    30,      120,       120]

        stand = dict(zip(servos, stand_angles))
        crouch = dict(zip(servos, crouch_angles))

        pos = stand if desired_position == "stand" else crouch

        for servo, angle in pos.items():
            self.servos[servo].move(angle)
                
            if self.servos[servo].get_physical_angle() != angle:
                raise ServoError(f"[MOVE] Servo {self.servos[servo].get_id()} 
                                    did not reach target angle.")
            

        # not sure which version of move_to_pos is more user friendly
        # this one is hardcoded, but straightforward
        # one above is somewhat more general, but maybe not enough to be worth it
        '''    self.servos['l_hip'].move(105)
            self.servos['r_hip'].move(150)
            
            self.servos['l_leg'].move(175)
            self.servos['r_leg'].move(5)
            
            self.servos['l_knee'].move(120)
            self.servos['r_knee'].move(120)

        elif position == "crouch":
            self.servos['l_hip'].move(110)
            self.servos['r_hip'].move(145)
            
            self.servos['l_leg'].move(150)
            self.servos['r_leg'].move(30)
            
            self.servos['l_knee'].move(120)
            self.servos['r_knee'].move(120)'''

        # TODO: ENSURE TARGET POS REACHED

    
    def boot(self):
        # run upon starting wall-e up
        for servo in self.servos.values():
            # ensure you can communicate with motors and that voltage is acceptable
            self.query_motor_position(servo)
            # TODO: enable/disable motors? ensure connected to power
            self.query_motor_voltage(servo)
        
        # flash sequence to signal that boot up was successful
        self.flash_thrice({'head': self.head, 'neck': self.neck})
        self.flash_thrice({'l_hip': self.lhip, 'l_leg': self.lleg, 'l_knee': self.lknee})
        self.flash_thrice({'r_hip': self.rhip, 'r_leg': self.rleg, 'r_knee': self.rknee})


    def homing(self):
        # ensure you can communicate with motors, then move wall-e to his home "stand" position
        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.move_to_pos("stand")


    def health_check(self):
        # ensure communication with motors, their temp, and their voltage are okay
        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.query_motor_temp(servo)
            self.query_motor_voltage(servo)

        # heartbeat flash to signal good health
        self.heartbeat()


    def shutdown(self):
        # ensure communication with motors, then move wall-e to his rest "crouch" position
        for servo in self.servos.values():
            self.query_motor_position(servo)
            self.move_to_pos("crouch")
            # TODO: disable motors?


    def walk(self):
        t = 0
        #offsetHip = 240
        #offsetUpperKnee = 15
        #offsetKnee = 15

        while t<15: 

            if t%2 == 0 :
                self.health_check()
                print("health good (for now)\n")
            
            self.servos['rleg'].move(4 * cos(2.5* t+pi/2) + 5)          # 
            self.servos['lleg'].move(4 * cos((2.5* t+pi/2)) + 175)      #
            
            self.servos['rhip'].move(8 * sin((2.5*t+pi/2)) + 150)       #
            self.servos['lhip'].move(8 * sin((2.5*t+pi/2)) + 105)       #
            
            self.servos['rknee'].move(10 * cos((2.5*t+pi/2)) + 120)     #
            self.servos['lknee'].move(10 * cos(2.5*t+pi/2) + 120)       # 

            time.sleep(0.05)
            t += 0.1


    #def move_backwards(servo_hip, servo_upper_knee, servo_knee): lol
    #    servo_hip.move(cos(t) * 60 + 60)
    #    servo_upper_knee.move(sin(t) * 60 + 60)
    #    servo_knee.move(cos(t) * 60 + 60)


def main():
    print("HI WALL-E!\n")
    walle = Walle()
    
    walle.boot()
    walle.homing()

    walle.walk()

    walle.shutdown()


if __name__ == "__main__":
    print("executing...")
    main()