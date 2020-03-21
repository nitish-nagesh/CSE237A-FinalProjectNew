from  big_servo_controller import BigServoController
from small_servo_controller import SmallServoController
from ultrasonic_controller import UltrasonicController

import threading
import time

class ActuatorManager():
    def __init__(self):
        self.big_servo = BigServoController()
        self.small_servo = SmallServoController()
        self.ultrasonic = UltrasonicController()

    def deterr_pests(self):
        self.ultrasonic.emit_sound()

        # threading approach, not needed with single blocking actuator
        #big_servo_thread = threading.Thread(target=self.big_servo.sweep, args=(2,1))
        #small_servo_thread = threading.Thread(target=self.small_servo.spin_for, args=(5,))
        #big_servo_thread.start()
        #small_servo_thread.start()
        #big_servo_thread.join()
        #small_servo_thread.join()

        self.small_servo.spin()
        self.big_servo.sweep(2, 1) #blocking
        self.small_servo.stop_spinning()
        self.ultrasonic.stop_emitting()

if __name__ == '__main__':
    import RPi.GPIO as GPIO
    manager = ActuatorManager()
    manager.deterr_pests()
    GIO.cleanup()
