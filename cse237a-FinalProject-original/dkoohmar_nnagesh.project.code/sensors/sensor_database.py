# sqlite code modified from sqlitetutorial.net/sqlite-python
# verify the sqlite db updated with 'sqlite3 sensor_data.db'
# sqlite> .tables (ensure sensor_data appears)
# sqlite> .header on
# sqlite> .mode column
# sqlite> SELECT * FROM sensor_data
# to get the last N records:
# select * from sensor_data order by timestamp desc limit N

import sqlite3
import sys
from sqlite3 import Error

class SensorDatabase():
    def __init__(self, database_file):
        try:
            self.conn = sqlite3.connect(database_file)
        except Error as e:
            print(e)
            sys.exit(1)
        sql_create_sensed_data_table = """CREATE TABLE IF NOT EXISTS sensor_data (
                                            id integer PRIMARY_KEY,
                                            timestamp text NOT NULL,
                                            motion_count integer NOT NULL,
                                            soil_moisture integer NOT NULL,
                                            ground_temp integer NOT NULL,
                                            air_temp integer NOT NULL, 
                                            humidity integer NOT NULL,
                                            air_pressure integer NOT NULL,
                                            uv_index integer NOT NULL,
                                            waterproof_temp integer NOT NULL
                                            );"""
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql_create_sensed_data_table)
        except Error as e:
            print("Error setting up database:\n")
            print(e)
            sys.exit(1)
        self.column_list = ['timestamp', 'motion_count', 'soil_moisture',
                            'ground_temp', 'air_temp', 'humidity','air_pressure',
                            'uv_index','waterproof_temp']

    def write_sensor_data(self, data):
        sql_insert_data = """ INSERT INTO sensor_data({})
                            VALUES(?,?,?,?,?,?,?,?,?)""".format(','.join(self.column_list))
        cursor = self.conn.cursor()
        cursor.execute(sql_insert_data, [data[column] for column in self.column_list])
        self.conn.commit()

    def read_sensor_data(self, column, entries):
        sql_read_data = "select {} from sensor_data order by timestamp desc".format(column)
        if entries > 0:
            sql_read_data += " limit {}".format(entries)
        cursor = self.conn.cursor()
        return cursor.execute(sql_read_data).fetchall()

    def close(self):
        self.conn.close()

if __name__ == '__main__':
    data = {'timestamp': '2020-02-29 22:21:55.000', 'motion_count': 3, 'soil_moisture': 372, 'ground_temp': 73, 'air_temp': 70, 'humidity': 42, 'air_pressure': 1004,   'uv_index': 1, 'waterproof_temp': 71}
    database = SensorDatabase('test_database.db')
    database.write_sensor_data(data)
    result = database.read_sensor_data(','.join(database.column_list), 1)[0]
    print("Read following values:")
    for idx, column in enumerate(database.column_list):
        print("\t{}:{}".format(column, result[idx]))
    database.close()

