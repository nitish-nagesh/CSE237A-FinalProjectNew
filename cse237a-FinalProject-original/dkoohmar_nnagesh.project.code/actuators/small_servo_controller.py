# Code modified from
# https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/

import RPi.GPIO as GPIO
import time

class SmallServoController():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        bcm_pin = 25
        GPIO.setup(bcm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(bcm_pin, 50) # 50hz servo, period 1/50.
        self.dc = 1 #duty cycle  

    def spin_for(self, duration):
        self.spin()
        time.sleep(duration)
        self.stop_spinning()
        
    def spin(self):
        self.pwm.start(self.dc) #initial duty cycle

    def stop_spinning(self):
        self.pwm.stop()

if __name__ == '__main__':
    small_servo = SmallServoController()
    small_servo.spin()
    time.sleep(5)
    small_servo.stop_spinning()
    GPIO.cleanup()
