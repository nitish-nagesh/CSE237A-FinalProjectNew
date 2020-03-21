# Code modified from
# https://thepihut.com/blogs/raspberry-pi-tutorials/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

import RPi.GPIO as GPIO
import time

class UltrasonicController():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.trigger_pin = 24
        self.echo_pin = 23
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    # emits at 40 khz
    def emit_sound(self):
        GPIO.output(self.trigger_pin, True)

    def stop_emitting(self):
        GPIO.output(self.trigger_pin, False)

if __name__ == '__main__':
    import time
    ultrasonic_control = UltrasonicController()
    ultrasonic_control.emit_sound()
    time.sleep(3)
    ultrasonic_control.stop_emitting()
    GPIO.cleanup()


