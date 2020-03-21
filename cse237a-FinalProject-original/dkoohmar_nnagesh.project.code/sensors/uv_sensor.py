# Code modified from
# https://github.com/THP-JOE/Python_SI1145/blob/master/examples/simpletest.py

import SI1145.SI1145 as SI1145
import sensor

class UVSensor(sensor.Sensor):
    def __init__(self):
        self.sensor = SI1145.SI1145()
    
    def get_data(self):
        data = {}
        # vis and IR need to be read before UV can be calculated
        self.sensor.readVisible()
        self.sensor.readIR()
        data['uv_index'] = self.sensor.readUV()

        return data

# test sensor
if __name__ == '__main__':
    uv_sensor = UVSensor()
    print(uv_sensor.get_data())
