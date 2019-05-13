# Usage:
# python eyes_tracking.py --full --mirror

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-fc", "--fclassifier", required = False, default="classifiers/haarcascade_frontalface_default.xml", help = "path to where the face cascade resides  (optional)")
ap.add_argument("-ec", "--eclassifier", required = False, default="classifiers/haarcascade_eye.xml", help = "path to where the eyes cascade resides  (optional)")
ap.add_argument("-v", "--video", required = False, help = "path to where the video resides  (optional)")
ap.add_argument("-m", "--mirror", required = False, action='store_true', help = "enable mirror mode  (optional)")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode  (optional)")
args = vars(ap.parse_args())

# Configure windows
windowName = "Eyes Tracking"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
 
# If --video is not supplied we will read video from the webcam.
# Otherwise, OpenCV will open the video file pointed by the --video argument
if (args["video"]):
    video = cv2.VideoCapture(args["video"])
else:
    video = cv2.VideoCapture(cv2.CAP_DSHOW)

# In order to build face and eyes recognition system, we use the built-in Haar cascade classifiers in OpenCV. 
facesClassifier = cv2.CascadeClassifier(args["fclassifier"])
eyesClassifier = cv2.CascadeClassifier(args["eclassifier"])

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

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting the actual faces in the frame 
    faces = facesClassifier.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30,30))

    # loop over the faces
    for (fx, fy, fw, fh) in faces:
        # Draw a rectangle surrounding each
        cv2.rectangle(frame, pt1 = (fx, fy), pt2 = (fx + fw, fy + fh), color = (0, 0, 255), thickness = 2)

        # Extract the face region of interest (ROI) from the image using NumPy array slicing
        # The faceROI variable cointains the bounding box region of the face
        # slicing[startY:endY, startX:endX]
        faceROI = gray[fy:fy + fh, fx:fx + fw]
        
        # Detecting the actual eyes in the frame 
        eyes = eyesClassifier.detectMultiScale(faceROI, scaleFactor = 1.3, minNeighbors = 5, minSize = (20,2cls0))

        # loop over the eyes
        for (ex,ey,ew,eh) in eyes:
            # Draw a rectangle surrounding each (OpenCV stores RGB pixels in reverse order)
            cv2.rectangle(frame, pt1 = (fx + ex, fy + ey), pt2 = (fx + ex + ew, fy + ey + eh), color = (0, 255, 0), thickness = 2)
    
    # Display the output
    cv2.imshow(windowName, frame)

    # Wait for a key press to finish program
    key = cv2.waitKey(5)
    if (key in [ord("q"), 27] or cv2.getWindowProperty(windowName,cv2.WND_PROP_VISIBLE) < 1) : break
    

# The reference to the video is released
video.release()

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()