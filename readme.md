# motion-detector-python


## Prerequisites
- Python 3+
- Pip Modules
	- cv2
	- pillow
	- math
	- operator
	- functools

<br>

### Usage

<br>

#### Basic example
```py
import motion_detector as md


def myfunc():
	print("Motion detected")


d = md.MotionDetector()
d.configure(cam_port = 0) # Specifying camera port. Even if not specifying, default is taken as 0.
d.start(callback = myfunc) # Starting detector loop here. Use the callback argument to set a function to be called upon detection of motion.  
# Further code execution will hold off until the callback function is called. If no callback is specified, the loop will not stop even if motion is detected.

```

<br>

#### Variations

<br>

After the `callback` function is called, the detector loop ends. If you want the detector to continue -
```py
import motion_detector as md


def myfunc(detector):
    print("Motion detected")
    # Restart detector 
    detector.stop()
    detector.start(callback = lambda: myfunc(detector))


d = md.MotionDetector()
d.start(callback = lambda: myfunc(d))

```

<br>

If you don't want to use the `callback` argument but still want to execute code even after starting the detector loop - 
```py
import motion_detector as md
import threading


def myfunc():
	print("Motion detected")


d = md.MotionDetector()
threading.Thread(target = d.start).start() # Starting parallel thread for detector

while True:
    if md.current_movement == True: # Checking current movement status 
        # Executes if movement detected
        myfunc() 
        d.stop() # Stopping detector loop

```

<br>

The detector determines 2 images different if the RMS(Root mean square) difference between the 2 images is greater than a certain value. You can set this value by doing - 
```py
d.configure(max_rms_diff = 15) # If not specified, default value taken is 7
```
In layman's terms, greater RMS diff means lower sensitivity and lower RMS diff means greater sensitivity. Setting the RMS diff too low can result in false detections, while setting it too high can result in no detections. 
