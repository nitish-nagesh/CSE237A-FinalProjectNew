# Code modified from
# https://github.com/adafruit/Adafruit_CircuitPython_seesaw/blob/master/examples/seesaw_soil_simpletest.py

import busio
import sensor
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw

class SoilMoistureSensor(sensor.Sensor):
    def __init__(self):
        i2c_bus = busio.I2C(SCL, SDA)
        self.ss = Seesaw(i2c_bus, addr=0x36)
    
    def get_data(self):
        data = {}
        # read moisture level through capacitive touch pad
        data['soil_moisture'] = self.ss.moisture_read()

        # read temperature from the chip temperature sensor
        temp_c = self.ss.get_temp()
        temp_f = 9.0/5.0 * temp_c + 32
        data ['ground_temp'] = int(temp_f)
        return data

# test sensor
if __name__ == '__main__':
    soil_sensor = SoilMoistureSensor()
    print(soil_sensor.get_data())
