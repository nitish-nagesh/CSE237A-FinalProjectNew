# Code modified from
# https://tutorials-raspberrypi.com/raspberry-pi-servo-motor-control/

import RPi.GPIO as GPIO
import time

class BigServoController():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        bcm_pin = 8
        GPIO.setup(bcm_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(bcm_pin, 50) # 50hz servo, period 1/50.
        #for the tower control servo, position 0 is 1.5ms pulse, "90" clockwise is 2ms, -90 counterclockwise is 1ms. 50hz = 20ms period. duty cycle = length/period * 100
        self.dc_initial = (1.5/20) * 100 # 2
        self.dc_clockwise = 10#(2/20) * 100 # 10
        self.dc_counter_clockwise = 2#(1/20) * 100 # 2    

    def sweep(self, duration, cycles):
        while cycles > 0:
            self.pwm.start(self.dc_initial) #initial duty cycle
            time.sleep(2)
            self.pwm.ChangeDutyCycle(self.dc_clockwise)
            time.sleep(duration)
            self.pwm.ChangeDutyCycle(self.dc_counter_clockwise)
            time.sleep(duration)
            self.pwm.ChangeDutyCycle(self.dc_clockwise)
            time.sleep(duration)
            self.pwm.ChangeDutyCycle(self.dc_initial)
            time.sleep(2)
            self.pwm.stop()
            cycles -= 1

if __name__ == '__main__':
    big_servo = BigServoController()
    big_servo.sweep(2,1)
    GPIO.cleanup()
