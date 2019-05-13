# Usage:
# python invisibility_cloak.py --mirror --full

# Import the necessary packages
import argparse
import numpy as np
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = False, help = "path to where the video resides (optional)")
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode  (optional)")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode  (optional)")
args = vars(ap.parse_args())

# Configure windows
windowName = "Harry Potter"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


# If --video is not supplied we will read video from the webcam.
# Otherwise, OpenCV will open the video file pointed by the --video argument
if (args["video"]):
    video = cv2.VideoCapture(args["video"])
else:
    video = cv2.VideoCapture(cv2.CAP_DSHOW)

time.sleep(3)

# Capturing and storing the static background frame
for i in range(60):
	(grabbed, background) = video.read()
	if (not args["video"] and args["mirror"]): background = cv2.flip(background, 1)

while True:
	# We read the next frame in the video by calling the read() method of camera
	(grabbed, frame) = video.read()

	# Detect if video finished
	if (args["video"] and not grabbed) : break

    # Mirror effect on webcam: Flip on Y axis
	if (not args["video"] and args["mirror"]) : frame = cv2.flip(frame, 1)

	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Generating mask to detect red color
	lower_red = (0,120,70)
	upper_red = (10,255,255)
	mask1 = cv2.inRange(hsv, lower_red, upper_red)

	lower_red = (170,120,70)
	upper_red = (180,255,255)
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1 + mask2

	# Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	mask2 = cv2.bitwise_not(mask1)

	# Generating the final output
	res1 = cv2.bitwise_and(background,background,mask= mask1)
	res2 = cv2.bitwise_and(frame,frame,mask= mask2)
	final = cv2.addWeighted(res1,1,res2,1,0)

	cv2.imshow(windowName, final)
	
	# Wait for a key press to finish program
	key = cv2.waitKey(1)
	if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1): break


# The reference to the video is released
video.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()