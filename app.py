#!flask/bin/python
import os
from flask import Flask , jsonify , request
from sense_hat import SenseHat
from flask_cors import CORS, cross_origin



app = Flask(__name__)
CORS(app)

sense = SenseHat()
sense.clear()


# get CPU temperature
def get_cpu_temp():
  res = os.popen("vcgencmd measure_temp").readline()
  t = float(res.replace("temp=","").replace("'C\n",""))
  return(t)

@app.route('/api')
def index():
    return "try with '/ambient' "

@app.route('/api/ambient', methods=['GET', 'OPTIONS'])
def get_ambient_params():
    t1 = sense.get_temperature_from_humidity()
    t2 = sense.get_temperature_from_pressure()
    t_cpu = get_cpu_temp()
    t = (t1+t2)/2
    temperature = t - ((t_cpu-t)/1.5)

    humidity = sense.get_humidity()

    pressure = sense.get_pressure()

    return jsonify({'temperature': temperature , 'humidity': humidity ,'pressure': pressure})

@app.route('/api/led/<rgb>', methods=['GET'])
def set_led_color(rgb):
    if rgb == 'red':
        X = [255, 0, 0]  # Red
    elif rgb == 'green':
        X = [0, 255, 0]  # green
    elif rgb == 'blue':
        X = [0, 0, 255]  # blue
    color = [
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X,
        X, X, X, X, X, X, X, X
        ]
    sense.set_pixels(color)
    return jsonify({'success': True })

@app.route('/api/led', methods=['POST'])
def set_led_message():
    if not request.json or not 'message' in request.json:
        abort(400)
    sense.show_message(request.json["message"], text_colour=[255, 255, 255])
    return jsonify({'success': True })

@app.route('/api/led/clear', methods=['GET'])
def set_led_clear():
    sense.clear()
    return jsonify({'success': True })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
