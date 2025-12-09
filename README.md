# Ball-Motion-Detection
Detects and shows trajectory of a ball and its speed in frames per second. 

# Features
Real time ball detection using HSV color masking.
Contour detection to identify the ball's position.
Trajectory drawing with stored position history.
Speed calculation using pixel distance and timestamps.
Lightweight Python implementation.
Works on webcam or video file input.

# Working
Frame captured from webcam
Converted to HSV color space
Largest contour detected is assumed to be the ball
Ball center tracked
Trajectory drawn using previous positions
Speed computed as distance(change in coordinates)/change in time

# Installation
git clone https://github.com/Pranshu3510/Ball-Motion-Detection.git 
cd Ball-motion-Detection
pip install -r requirements.txt
