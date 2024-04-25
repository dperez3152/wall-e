from math import sin, cos
from lx16a import *
import time

LX16A.initialize("/dev/ttyUSB0", 1)

# servo 1: top head
# servo 2: right shin   120
# servo 3: right leg    180
# servo 4: left leg     0
# servo 5: left shin    120
# servo 6: head lifter
# servo 7: right hip    120
# servo 8: left hip     120

try:
    servo1 = LX16A(4)
    servo2 = LX16A(5)
    servo3 = LX16A(8)
    servo1.set_angle_limits(0, 360)
    servo2.set_angle_limits(0, 360)
    servo3.set_angle_limits(0, 360)

except ServoTimeoutError as e:
    print(f"Servo {e.id_} is not responding. Exiting...")
    quit()

t = 0
while t <0.11:
    #print(servo1.get_physical_angle(), servo1.get_angle_offset(True))
    print("\nupper knee:")
    print(servo2.get_physical_angle(), servo2.get_angle_offset(True))
    print("knee:")
    print(servo3.get_physical_angle(), servo3.get_angle_offset(True))
    #servo2.move(10)
    #servo1.move(sin(t) * 60 + 60)
    #servo1.move(sin(t) * 60 + 60)
    #servo2.move(cos(t) * 60 + 60)

    time.sleep(0.05)
    t += 0.05
