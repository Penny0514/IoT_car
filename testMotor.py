import RPi.GPIO as gpio
import time
from flask import Flask, render_template, Response, request
from camera_pi import Camera

N1 = 17
N2 = 22
N3 = 23
N4 = 24
TRIG = 26
ECHO = 3

gpio.setwarnings(False)
gpio.setmode(gpio.BCM)
gpio.setup(N1, gpio.OUT)
gpio.setup(N2, gpio.OUT)
gpio.setup(N3, gpio.OUT)
gpio.setup(N4, gpio.OUT)
gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)
pwm1 = gpio.PWM(N2, 100)
pwm2 = gpio.PWM(N3, 100)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def init():
    gpio.setmode(gpio.BCM)
    gpio.setup(N1, gpio.OUT)
    gpio.setup(N2, gpio.OUT)
    gpio.setup(N3, gpio.OUT)
    gpio.setup(N4, gpio.OUT)
    gpio.setup(TRIG, gpio.OUT)
    gpio.setup(ECHO, gpio.IN)


@app.route('/forward', methods=['GET', 'POST'])
def forward():
    init()

    while(distance() > 25):
        gpio.output(N1, False)
        gpio.output(N2, True)
        gpio.output(N3, True)
        gpio.output(N4, False)
        time.sleep(0.5)

    stop()
    autoBack(0.5)
    return render_template('index.html')


@app.route('/back', methods=['GET', 'POST'])
def back():
    gpio.cleanup()
    init()
    gpio.output(N1, True)
    gpio.output(N2, False)
    gpio.output(N3, False)
    gpio.output(N4, True)
    return render_template('index.html')


@app.route("/left", methods=['GET', 'POST'])
def left():
    gpio.cleanup()
    init()
    gpio.output(N1, False)
    gpio.output(N2, True)
    gpio.output(N3, False)
    gpio.output(N4, True)
    return render_template('index.html')


@app.route("/right", methods=['GET', 'POST'])
def right():
    gpio.cleanup()
    init()
    gpio.output(N1, True)
    pwm1.stop()
    pwm2.start(0)
    pwm2.ChangeDutyCycle(90)
    gpio.output(N4, False)
    return render_template('index.html')


@app.route("/stop", methods=['GET', 'POST'])
def stop():

    init()
    gpio.output(N1, False)
    gpio.output(N4, False)
    gpio.cleanup()
    pwm1.stop()
    pwm2.stop()
    return render_template('index.html')


def autoBack(t):
    gpio.cleanup()
    init()
    gpio.output(N1, True)
    gpio.output(N2, False)
    gpio.output(N3, False)
    gpio.output(N4, True)
    time.sleep(t)
    gpio.cleanup()


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def speed():
    value = request.form['speed']
    speed = int(value)*10
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)
    print("value", value)
    return render_template('index.html')


@app.route('/controlSpeed', methods=['POST'])
def controlSpeed():
    value = request.form['speed']
    speed = int(value)*10

    init()

    while(distance() > 25):
        gpio.output(N1, False)
        pwm1.start(0)
        pwm1.ChangeDutyCycle(speed)
        pwm2.start(0)
        pwm2.ChangeDutyCycle(speed)
        gpio.output(N4, False)
        time.sleep(0.5)

    stop()
    autoBack(0.5)
    return render_template('index.html')


def distance():
    gpio.output(TRIG, True)
    time.sleep(0.00001)
    gpio.output(TRIG, False)

    start = time.time()
    stop = time.time()

    while gpio.input(ECHO) == 0:
        start = time.time()
    while gpio.input(ECHO) == 1:
        stop = time.time()

    timeElapsed = stop - start
    distance = (timeElapsed*34300)/2
    print(distance)
    return distance


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
