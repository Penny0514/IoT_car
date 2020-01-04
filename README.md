# IoT_car
## Inteoduction
This is a redio control car, which you can control it on your mobile phone 
### Features
1. A camera is set at the front of the car to stream the video on your phone, so you can see if there is any obstacle
2. A sensor can help you to stop automatically to avoid collision
3. You can control the speed of motors by slider on the web interface
### Prepare
- 四驅自走車
- 直流馬達*4
- 鏡頭*2
- 電池盒*2
- 電池*8
- 超音波感測器
- L298N 馬達驅動板
- 杜邦線
- 麵包板
## Before Getting Start
The first thing to do is to install Flask on your Raspberry Pi. Go to Terminal and enter:
```python
sudo apt-get install python3-flask
```
Create a new folder to start your project
```
mkdir webapp
```
Go to the file you created, and new folders **templates** and **statics**
These two files must under the folder **webapp**
```
cd webapp
mkdir templates
mkdir statics
```
## Build up your Car
Click this link to learn how to build the car kit
 https://www.youtube.com/watch?v=uW8YVcBjPGU

## L298N motor driver
In order to control your motor, you need to use L298N
One motor driver can help us to control our motor in two parts. It depends on the way you connect Dupont Lines.
In this project, I devided four motors into left side and right side. It can make sure that this car can turn left or turn right
> Note: Make sure that wheels on the same side turn in the same direction

Click this link for more detail
https://www.youtube.com/watch?v=bNOlimnWZJE&list=PLc6fhBPeC6SBbZFcrHLlPXyR2svfxf1RZ&index=19&t=507s

## Sensor
![](81618198_3802171866460465_14051518084808704_n.jpg)
Define pins that are connected with sensor on the respberry pi
```
TRIG = 26
ECHO = 3
gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)
```

We need to initiate the TRIG pin for ready to sensor 
> Before turn the signal *True* to *False*, stay for a millisecond
```
def distance():
    gpio.output(TRIG, True)
    time.sleep(0.00001)
    gpio.output(TRIG, False)
```

Calculate the time of distance with the formula
> **Distance = Time X 34300 / 2**

Return the result in the end of the function
```
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
```

## Video Streaming

**testMotor2.py**
```
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

```
The above script streams your camera video on an **index.html** page as below:
``` 
<img src="{{ url_for('video_feed') }}" width="50%" />
```
Click this link for more detail
https://www.instructables.com/id/Video-Streaming-Web-Server/
