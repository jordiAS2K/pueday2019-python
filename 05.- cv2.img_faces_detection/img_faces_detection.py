# Usage:
# python img_faces_detection.py --image images/people-001.jpg --full
# python img_faces_detection.py --image images/people-002.jpg --full
# python img_faces_detection.py --image images/people-003.jpg --full
# python img_faces_detection.py --image images/people-004.jpg --full
# python img_faces_detection.py --image images/people-005.jpg --full
# python img_faces_detection.py --image images/people-006.jpg --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-fc", "--fclassifier", required = False, default="classifiers/haarcascade_frontalface_default.xml", help = "path to where the face cascade resides")
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Faces Detector"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Loading the image using OpenCV
image = cv2.imread(args["image"])

# Convert image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# In order to build face recognition system, we use the built-in Haar cascade classifiers in OpenCV. 
# Luckily, these classifiers have already been pre-trained to recognize faces!
# OpenCV repository: https://github.com/opencv/opencv
# data\haarcascades: This folder contains trained classifiers for detecting objects
#                    of a particular type, e.g. faces (frontal, profile), pedestrians etc
#
# Building our own classifier is certainly outside the scope. But if we wanted to, we would need a
# lot of “positive” and “negative” images. Positive images would contain images with faces, whereas 
# negative images would contain images without faces. 
# Based on this dataset, we could then extract features to characterize the face (or lack of face) in an image 
# and build our own classifier. 
facesClassifier = cv2.CascadeClassifier(args["fclassifier"])

# “sliding window” approach
# These classifiers work by scanning an image from left to right, and top to bottom, at varying scale sizes. 
# As the window moves from left to right and top to bottom, one pixel at a time, the classifier is asked whether or
# not it “thinks” there is a face in the current window

# Detecting the actual faces in the image is handled by making a call to the detectMultiScale method of
# our classifier created. We supplies his scaleFactor, minNeighbors and minSize, then the method takes care of 
# the entire face detection process for us!
faces = facesClassifier.detectMultiScale(gray, scaleFactor = 1.3, minNeighbors = 5, minSize = (30,30))

# The detectMultiScale method then returns rects, a list of tuples containing the bounding boxes of the faces 
# in the image. These bounding boxes are simply the (x, y) location of the face, along with the width and height of the box.
print(f"I found {len(faces)} face(s)")

# loop over the faces and draw a rectangle surrounding each
for (i, (x, y, w, h)) in enumerate(faces):
    cv2.rectangle(image, pt1 = (x, y), pt2 = (x + w, y + h), color = (0, 0, 255), thickness = 2)
    cv2.putText(image, text = f"Face #{i}", org = (x, y - 10), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.7, color = (0, 0, 255), thickness = 1)

# Display the image to our screen
cv2.imshow(windowName, image)

# Wait for a key press to finish program
cv2.waitKey(0)

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()