import threading
import time
import sqlite3
import sys
from sensor_database import SensorDatabase

class SensorManager:
    # takes a period in seconds to sample all registered sensors
    # and stores the period's samples in a sqllite record
    def __init__(self, period, database_filename):
        self.running = False
        self.period = period # seconds
        self.sensors = []
        self.thread = threading.Thread(target=self.collect_data)
        self.database_filename = database_filename

    def add_sensor(self, sensor):
        if sensor not in self.sensors:
            self.sensors.append(sensor)

    def start_collecting(self):
        self.running = True
        self.thread.start()

    def stop_collecting(self):
        self.running = False
        self.thread.join()

    def collect_data(self):
        #sqlite3 requires conn to be created from the same thread the data is written from
        database = SensorDatabase(self.database_filename)
        elapsed = self.period # use elapsed for blocking sleep of shorter time
        while self.running:
            if elapsed == self.period:
                data = {}
                data['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S.000') #https://www.sqlite.org/datatype3.html
                for sensor in self.sensors:
                    data.update(sensor.get_data())
                database.write_sensor_data(data)
                print("="*50)
                print("Collected the following data:")
                for sensor,value in data.items():
                    print("\t{}: {}".format(sensor, value))
                elapsed = 0
            time.sleep(1)
            elapsed += 1 # seconds
        database.close()

if __name__ == '__main__':
    import signal
    import RPi.GPIO as GPIO
    from motion_sensor import MotionSensor
    from temp_humidity_pressure_sensor import TempHumidityPressureSensor
    from soil_moisture_sensor import SoilMoistureSensor
    from uv_sensor import UVSensor
    from waterproof_temp_sensor import WaterproofTempSensor
    from sensor_database import SensorDatabase
    
    # initialize all sensors
    motion_sensor = MotionSensor()
    temp_humidity_pressure_sensor = TempHumidityPressureSensor()
    soil_moisture_sensor = SoilMoistureSensor()
    uv_sensor = UVSensor()
    waterproof_temp_sensor = WaterproofTempSensor()
    
    manager = SensorManager(5 * 60, 'test_database.db') # sample every 5 minutes
    manager.add_sensor(motion_sensor)
    manager.add_sensor(temp_humidity_pressure_sensor)
    manager.add_sensor(soil_moisture_sensor)
    manager.add_sensor(uv_sensor)
    manager.add_sensor(waterproof_temp_sensor)
    manager.start_collecting()

    def signal_handler(signal, frame):
        manager.stop_collecting()
        GPIO.cleanup()

    signal.signal(signal.SIGINT, signal_handler)
