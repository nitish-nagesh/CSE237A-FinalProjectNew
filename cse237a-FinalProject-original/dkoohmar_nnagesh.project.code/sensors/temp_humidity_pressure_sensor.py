# code modified from
# https://learn.adafruit.com/adafruit-bme280-humidity-barometric-pressure-temperature-sensor-breakout/python-circuitpython-test#python-installation-of-bme280-library-5-10

import board
import busio
import adafruit_bme280
import sensor

class TempHumidityPressureSensor(sensor.Sensor):
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
    
    def get_data(self):
        data = {}

        temp_c = self.bme280.temperature
        temp_f = 9.0/5.0 * temp_c + 32
        data['air_temp'] = int(temp_f)
        data['humidity'] = int(self.bme280.humidity)
        data['air_pressure'] = int(self.bme280.pressure)

        return data

# test sensor
if __name__ == '__main__':
    temp_humidity_pressure_sensor = TempHumidityPressureSensor()
    print(temp_humidity_pressure_sensor.get_data())
