# Flask-ROS2 video stream
Flask based webinterface for ROS2 Video Stream 

## Prerequisite
There are some libraries and frameworks required for the program work properly.

**Frameworks**
 - ROS2 Eloquent
 - Flask
 - Gunicorn
 - OpenCV
 
**Python3 Libraries**
 - Cvbridge
 - Threading
 - Signals

## Building

To build the project, we must follow this steps:

**Terminal 1:**

```sh
$ cd ~/your_workspace/
$ colcon build
$ . install/setup.bash
```

After that, the two packages of the workspace are builded and the cam2imge node is initialized.

For run the subscriber node and host the website, we must follow this steps in another terminal.

**Terminal 2:**

```sh
$ cd src/video_stream_ros2/video_stream_ros2/
$ gunicorn --threads 5 --workers 1 --bind your_ip:8080 app:app
```

The last command uses the [Gunicorn](https://gunicorn.org/), a framework that act like a Python WSGI HTTP Server for UNIX. Replace **your_ip** by yours machine ip.
