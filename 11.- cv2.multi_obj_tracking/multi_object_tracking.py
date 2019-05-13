# Documentation: https://www.pyimagesearch.com/2018/08/06/tracking-multiple-objects-with-opencv/
# USAGE
# python multi_object_tracking.py --video videos/soccer-01.mp4 --tracker csrt --full
# python multi_object_tracking.py --video videos/soccer-02.mp4 --tracker csrt --full
# python multi_object_tracking.py --video videos/soccer-01.mp4 --tracker csrt --full
# python multi_object_tracking.py --video videos/race-100m.mp4 --tracker csrt --full

# import the necessary packages
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required = False, help = "path to where the video resides  (optional)")
ap.add_argument("-s", "--speed", type = int, default = 5, choices=[1,5,50,100,150,200,250,300], required = False, help = "video reproduction speed")
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode  (optional)")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode  (optional)")
ap.add_argument("-t", "--tracker", type=str, required = False, default="csrt",	help="OpenCV object tracker type (oprtional)")
args = vars(ap.parse_args())

# Configure windows
windowName = "Multi Tracking"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
# I recommend the following three algorithms:
#  KCF: Fast and accurate
#  CSRT: More accurate than KCF but slower
#  MOSSE: Extremely fast but not as accurate as either KCF or CSRT
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}


# Initialize OpenCV's special multi-object tracker
# The class allows us to:
#   Add new object trackers to the MultiTracker
#   Update all object trackers inside the MultiTracker  with a single function cal
trackers = cv2.MultiTracker_create()

# If --video is not supplied we will read video from the webcam.
# Otherwise, OpenCV will open the video file pointed by the --video argument
if (args["video"]):
	video = cv2.VideoCapture(args["video"])
else:
    video = cv2.VideoCapture(cv2.CAP_DSHOW)

# loop over frames from the video stream
while True:
	# grab the current frame, then handle if we are using a
	# VideoStream or VideoCapture object
	(grabbed, frame) = video.read()

	# Detect if video finished
	if (args["video"] and not grabbed):	break

    # Mirror effect on webcam: Flip on Y axis
	if (not args["video"] and args["mirror"]): frame = cv2.flip(frame,1)

	# grab the updated bounding box coordinates (if any) for each
	# object that is being tracked
	# The update  method will locate the object’s new position and return a success boolean 
	# and the bounding box  of the object.
	(success, boxes) = trackers.update(frame)

	# loop over the bounding boxes and draw then on the frame
	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	# show the output frame
	cv2.imshow(windowName, frame)
	key = cv2.waitKey(args["speed"])

	# if the 's' key is selected, we are going to "select" a bounding
	# box to track
	if key == ord("s"):

		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
		box = cv2.selectROI(windowName, frame, fromCenter=False, showCrosshair=True)

		# create a new object tracker for the bounding box and add it
		# to our multi-object tracker
		tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
		trackers.add(tracker, frame, box)

	# if the `q` key was pressed, break from the loop
	elif (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1):
		break

video.release()

# close all windows
cv2.destroyAllWindows()