from sklearn.linear_model import LinearRegression
from flask import Flask, render_template, g, request
import numpy
import sys
sys.path.insert(0,'../sensors')
from sensor_database import SensorDatabase


app = Flask(__name__)

def get_sensor_database():
    sensor_database = getattr(g, '_database', None)
    if sensor_database is None:
        sensor_database = SensorDatabase('../sensor_data.db')
    return sensor_database

@app.teardown_appcontext
def close_connection(exception):
    sensor_database = getattr(g, '_database', None)
    if sensor_database is not None:
        sensor_database.close()

@app.route("/")
def home():
    sensor_database = get_sensor_database()
    # Access last 100 database entries
    sensor_data = {}
    for column in sensor_database.column_list:
        if column == 'timestamp':
            continue
        sensor_data[column] = sensor_database.read_sensor_data('timestamp,'+column, 100)
        #break # debug only
    return render_template("index.html", sensor_data=sensor_data, prediction_types=sensor_database.column_list[1:], predicted='')

@app.route("/status/<string:data_type>")
def status(data_type):
    sensor_database = get_sensor_database()
    sensor_data = {}
    data[data_type] = sensor_database.read_sensor_data('timestamp,'+data_type, 100)
    # pass column data to template
    return render_template("index.html", sensor_data=sensor_data, prediction_types=sensor_database.column_list[1:], predicted='')

@app.route("/prediction", methods=['POST'])
def prediction():
    column = request.form['sensor_prediction']
    sensor_database = get_sensor_database()
    # Access last 100 database entries
    sensor_data = sensor_database.read_sensor_data(column, 100)
    
    sensor_data_clean = [x[0] for x in sensor_data]
    time_units =  [x for x in range(len(sensor_data))]
    sensor_data_arr = numpy.array(sensor_data_clean).reshape((-1, 1))
    time_units_arr = numpy.array(time_units).reshape((-1,1))

    model = LinearRegression()
    model.fit(time_units_arr, sensor_data_arr)
    
    # Predict 50 time values
    start_prediction = len(sensor_data)
    predicted = model.predict([[x] for x in range(start_prediction, start_prediction + 50)])

    # Add timestamp to prediction
    sensor_data_predicted_timestamped = [(x*5,predicted[x-1][0]) for x in range(1, len(predicted)+1)]
    sensor_data_predicted = {}
    sensor_data_predicted[column] = sensor_data_predicted_timestamped
    return render_template("index.html", sensor_data=sensor_data_predicted, prediction_types=sensor_database.column_list[1:], predicted='True')
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
