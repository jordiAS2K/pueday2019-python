# Usage:
# python load_cam.py --mirror --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Webcam Visualizer"
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
    if (args["mirror"]):
        frame = cv2.flip(frame,1)

    # Display the output
    cv2.imshow(windowName, frame)

    # Wait for a key press to finish program
    key = cv2.waitKey(1)
    if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1) :
        break
    

# The reference to the video is released
cam.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()