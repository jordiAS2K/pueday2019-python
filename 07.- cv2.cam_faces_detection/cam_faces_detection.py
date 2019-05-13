# Usage:
# python cam_faces_detection.py --mirror --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-fc", "--fclassifier", required = False, default="classifiers/haarcascade_frontalface_default.xml", help = "path to where the face cascade resides")
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Webcam: Face Detector"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 

# Loading the video using OpenCV
# If you supply an integer value of 0 instructs OpenCV to read from webcam device, whereas supplying
# a string indicates that OpenCV should open the video the path points to
# Change param to: 
#  cv2.CAP_ANY   == 0    (Auto detect)
#  cv2.CAP_DSHOW == 700  DirectShow (via videoInput)
cam = cv2.VideoCapture(cv2.CAP_DSHOW)

# In order to build face recognition system, we use the built-in Haar cascade classifiers in OpenCV. 
# Luckily, these classifiers have already been pre-trained to recognize faces!
facesClassifier = cv2.CascadeClassifier(args["fclassifier"])

# Display the webcam to our screen
# Start to lopping over all frames in the webcam.
# At most basic level, a video is simply a sequence of images put together
while True:
    # We read the next frame in the video by calling the read() method of camera
    # The read method returns a tuple of two values:
    #   grabbed: a boolean indicating whether reading the frame was successfule
    #   frame:   which is the frame itself
    (grabbed, frame) = cam.read()

    # Mirror effect: Flip on Y axis
    if (args["mirror"]): frame = cv2.flip(frame,1)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting the actual faces in the frame 
    faces = facesClassifier.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30))

    # loop over the faces and draw a rectangle surrounding each
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, pt1 = (x, y), pt2 = (x + w, y + h), color = (0, 0, 255), thickness = 2)
    
    # Display the output
    cv2.imshow(windowName, frame)

    # Wait for a key press to finish program
    key = cv2.waitKey(1)
    if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1) : break
    

# The reference to the video is released
cam.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()