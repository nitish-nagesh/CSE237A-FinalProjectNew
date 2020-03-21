# Code modified from
# https://www.circuitbasics.com/raspberry-pi-ds18b20-temperature-sensor-tutorial/

import os
import glob
import time
import sensor

class WaterproofTempSensor(sensor.Sensor):
    def __init__(self):
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')
         
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')[0]
        self.device_file = device_folder + '/w1_slave'

    def read_temp_raw(self):
        f = open(self.device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines
    
    def get_data(self):
        data = {}
        
        lines = self.read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            data['waterproof_temp'] = int(temp_f)
        else:
            data['waterproof_temp'] = 0

        return data

# test sensor
if __name__ == '__main__':
    waterproof_temp_sensor = WaterproofTempSensor()
    print(waterproof_temp_sensor.get_data())
