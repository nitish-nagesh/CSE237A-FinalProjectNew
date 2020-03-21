# to startup when the pi starts up:
# sudo nano /etc/rc.local
# before the exit 0 line add: 
# python3 /home/pi/Documents/Github/237AGroupProject/saage.py &

import sys
sys.path.insert(0,'./sensors')
sys.path.insert(0,'./actuators')
import RPi.GPIO as GPIO
import signal

from actuator_manager import ActuatorManager
from sensor_manager import SensorManager
from motion_sensor import MotionSensor
from temp_humidity_pressure_sensor import TempHumidityPressureSensor
from soil_moisture_sensor import SoilMoistureSensor
from uv_sensor import UVSensor
from waterproof_temp_sensor import WaterproofTempSensor

COLLECTION_PERIOD = 5 * 60 # collect data every 5 minutes
DATABASE_FILE = 'sensor_data.db'

if __name__ == '__main__':
    # instantiate managers & sensors, then start collecting data
    actuator_manager = ActuatorManager()
    sensor_manager = SensorManager(COLLECTION_PERIOD, DATABASE_FILE)

    motion_sensor = MotionSensor(actuator_manager.deterr_pests)
    temp_humidity_pressure_sensor = TempHumidityPressureSensor()
    soil_moisture_sensor = SoilMoistureSensor()
    uv_sensor = UVSensor()
    waterproof_temp_sensor = WaterproofTempSensor()

    sensor_manager.add_sensor(motion_sensor)
    sensor_manager.add_sensor(temp_humidity_pressure_sensor)
    sensor_manager.add_sensor(soil_moisture_sensor)
    sensor_manager.add_sensor(uv_sensor)
    sensor_manager.add_sensor(waterproof_temp_sensor)

    print("Starting to collect data every {} seconds...".format(COLLECTION_PERIOD))
    sensor_manager.start_collecting() # blocks until a ^C is received
    
    def signal_handler(signal, frame):
        print("Stopping data collection, cleaning up GPIO...")
        sensor_manager.stop_collecting()
        GPIO.cleanup()

    signal.signal(signal.SIGINT, signal_handler)
