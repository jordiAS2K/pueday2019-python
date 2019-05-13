# Usage:
# python obj_tracking.py --mirror --full

# Import the necessary packages
import argparse
import numpy as np
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = False, help = "path to where the video resides (optional)")
ap.add_argument("-t", "--threshold", required = False, action='store_true', help = "show threshold images  (optional)")
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode  (optional)")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode  (optional)")
args = vars(ap.parse_args())

# Configure windows
windowName = "Object tracking"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 

# The object that will be tracking is a "yellow" object. Since this color isn't prevalent
# in any other location in the video besides this object, we wants to track shades of yellow
# We define the lower and upper limits of the shades of yellow in the RGB color space
# In this case, we defines colors as "yellow" if they are greather than RGB(0,67,100) and less than RGB(255,0,128)
colorLower = (20, 100, 100)
colorUpper = (30, 255, 255)


# If --video is not supplied we will read video from the webcam.
# Otherwise, OpenCV will open the video file pointed by the --video argument
if (args["video"]):
    video = cv2.VideoCapture(args["video"])
else:
    video = cv2.VideoCapture(cv2.CAP_DSHOW)

# Display the video or webcam to our screen
# Start to lopping over all frames in the video or webcam.
# At most basic level, a video is simply a sequence of images put together
while True:
    # We read the next frame in the video by calling the read() method of camera
    # The read method returns a tuple of two values:
    #   grabbed: a boolean indicating whether reading the frame was successfule
    #   frame:   which is the frame itself
    (grabbed, frame) = video.read()

    # Detect if video finished
    if (args["video"] and not grabbed): break

    # Mirror effect on webcam: Flip on Y axis
    if (not args["video"] and args["mirror"]): frame = cv2.flip(frame,1)

    # Find shades of the yellow in the frame using the cv2.inRange function
    # The result is a thresholded image with pixels falling within the upper and lower
    # range set to white and pixels that do not fall into this range se as black
    threshold = cv2.inRange(frame, colorLower, colorUpper)
    threshold = cv2.GaussianBlur(threshold, (3,3), 0)

    # Display threshold images
    if (args["threshold"]): cv2.imshow("threshold", threshold)

    # Now that we have the thresholded image, we needs to find the largest contour in the image
    # Assumption: the largest contour corresponds to the outline of the object that we want to track
    # We clone the thresholded image using the copy() method since the cv2.findContours function is destructive
    # to the NumPy array
    (contours, h) = cv2.findContours(threshold.copy(), mode = cv2.RETR_EXTERNAL, method = cv2.CHAIN_APPROX_SIMPLE)
    if (len(contours) > 0) :
        # Each individual contour is a Numpy array of (x,y) coordinates of boundary points of the object.
        # The contours are sorted in reverse order (largest first) using the cv2.contourArea function
        # to compute the area of the contour. Contours with larger areas are stored at the front of the list
        contour = sorted(contours, key = cv2.contourArea, reverse = True)[0]

        # To draw the contours, cv2.drawContours function is used. 
        # Its first argument is source image, second argument is the contours which should be passed as a Python list, 
        # third argument is index of contours (useful when drawing individual contour. To draw all contours, pass -1) 
        # and remaining arguments are color, thickness etc.
        rect = np.int32(cv2.boxPoints(cv2.minAreaRect(contour)))
        cv2.drawContours(frame, contours = [rect], contourIdx = -1, color = (0, 255, 0), thickness = 2)
    
    cv2.imshow(windowName, frame)

    
    # Wait for a key press to finish program
    key = cv2.waitKey(1)
    if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1): break
    

# The reference to the video is released
video.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()