#!/usr/bin/env python3

# Imports for ROS2
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image

# Imports for OpenCV operations
import cv2
from cv_bridge import CvBridge

# Imports for threading operations
import signal, sys
from threading import Thread, Event

# Import for flask application
from flask import Flask, render_template, Response


frame = None # Global variable frame (the holy image)

# Objects of cvbridge and event
bridge = CvBridge()
event = Event()


## Function that convert the message to image
def on_image(msg):
    global frame
    
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding = "passthrough")
    frame = cv2.imencode(".jpg",cv_image)[1].tobytes()
    event.set()

# Initializing the node
rclpy.init(args=None)
node = rclpy.create_node('Show_image_python')

Thread(target=lambda:node).start() # Starting the Thread with a target in the node

subscription = node.create_subscription(Image,"/image", on_image, 10) # Creating the Subscribe node

app = Flask(__name__) # Initializing the Flask application

## Function that runs 'spin_once' and waits for a new frame
def get_frame():
    rclpy.spin_once(node,timeout_sec=1.0)
    event.wait()
    event.clear()
    return frame

## Function that loads the template (Flask app)
@app.route('/')
def index():
    return render_template('index.html')

## Function that prepare the frame to be loaded into template
def gen():
    while True:
        frame = get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


## Function that insert the new frame in template
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

## Function that finish the actual context
def signal_handler(signal, frame):
    rclpy.shutdown()
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler) # Calls the 'signal_handler' and finish the actual signal (like a Ctrl + C)
 
## Main funcion, only initiate the Flask app
def main(args=None):
    app.run(host='0.0.0.0', port=8080 ,debug=True)


if __name__ == '__main__':
    main()












