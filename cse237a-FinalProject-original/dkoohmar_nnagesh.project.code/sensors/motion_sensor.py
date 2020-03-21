# Code modified from
# https://thepihut.com/blogs/raspberry-pi-tutorials/raspberry-pi-gpio-sensing-motion-detection

import RPi.GPIO as GPIO
import sensor
import time
               
def print_motion():
    print("Motion detected!")
               
class MotionSensor(sensor.Sensor):
    # Note: for raspberry pi, the pir sensors must be far from the pi or noise from the pi causes detection
    # The manager_callback is a no arg function used to trigger actuation from the actuation manager
    def __init__(self, manager_callback=print_motion):
        GPIO.setmode(GPIO.BCM)
        PIR_PIN = 17
        GPIO.setup(PIR_PIN, GPIO.IN)
        time.sleep(2)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=self.motion_detected)
        self.manager_callback = manager_callback
        self.motion_count = 0
    
    def motion_detected(self, pin):
        self.motion_count += 1
        self.manager_callback()
    
    def get_data(self):
        data = {}
        data['motion_count'] = self.motion_count
        self.motion_count = 0 # reset motion count every sampling period
        return data

# test sensor
if __name__ == '__main__':
    motion_sensor = MotionSensor()
    print(motion_sensor.get_data())
    GPIO.cleanup()
