# Usage:
# python load_video.py --video videos/video-001.mp4 --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = True, help = "path to where the video resides")
ap.add_argument("-s", "--speed", type = int, default = 25, choices=[1,5,10, 15, 25, 50,100,150,200,250,300], required = False, help = "video reproduction speed")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Video Visualizer"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  
  
# Loading the video using OpenCV
# If you supply an integer value of 0 instructs OpenCV to read from webcam device, whereas supplying
# a string indicates that OpenCV should open the video the path points to
video = cv2.VideoCapture(args["video"])


# Display the video to our screen
# Start to lopping over all frames in the video.
# At most basic level, a video is simply a sequence of images put together
while video.isOpened():
    # We read the next frame in the video by calling the read() method of camera
    # The read method returns a tuple of two values:
    #   grabbed: a boolean indicating whether reading the frame was successfule
    #   frame:   which is the frame itself
    (grabbed, frame) = video.read()

    # Display the output
    cv2.imshow(windowName, frame)

    # Wait for a key press to finish program
    key = cv2.waitKey(args["speed"])
    if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1) :
        break
    

# The reference to the video is released
video.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()