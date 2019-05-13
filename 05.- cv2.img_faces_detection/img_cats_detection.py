# Documentation:
# https://www.pyimagesearch.com/2016/06/20/detecting-cats-in-images-with-opencv/
# Usage:
# python img_cats_detection.py --image images/cats-001.jpg --full
# python img_cats_detection.py --image images/cats-002.jpg --full
# python img_cats_detection.py --image images/cats-003.jpg --full
# python img_cats_detection.py --image images/cats-004.jpg --full
# python img_cats_detection.py --image images/cats-005.jpg --full
# python img_cats_detection.py --image images/cats-006.jpg --full

# Import the necessary packages
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-cc", "--cclassifier", required = False, default="classifiers\\haarcascade_frontalcatface.xml", help = "path to where the cat cascade resides")
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# Configure windows
windowName = "Cats Detector"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Loading the image using OpenCV
image = cv2.imread(args["image"])

# Convert image to grayscale
# A normal pre-processing step before passing the image to a Haar cascade classifier, although not strictly required
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# In order to build cat recognition system, we use the built-in Haar cascade classifiers in OpenCV. 
# Luckily, these classifiers have already been pre-trained to recognize cat faces!
# OpenCV repository: https://github.com/opencv/opencv
# data\haarcascades: This folder contains trained classifiers for detecting objects
#                    of a particular type, e.g. faces (frontal, profile), pedestrians etc
#
# Load the cat detector Haar cascade
catsClassifier = cv2.CascadeClassifier(args["cclassifier"])

# Then detect cat faces
cats = catsClassifier.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 4, minSize = (30,30))

# The detectMultiScale method then returns rects, a list of tuples containing the bounding boxes of the cats 
# in the image. These bounding boxes are simply the (x, y) location of the cat face, along with the width and height of the box.
print(f"I found {len(cats)} cat(s)")

# loop over the cat faces and draw a rectangle surrounding each
for (i, (x, y, w, h)) in enumerate(cats):
    cv2.rectangle(image, pt1 = (x, y), pt2 = (x + w, y + h), color = (0, 0, 255), thickness = 2)
    cv2.putText(image, text = f"Cat #{i}", org = (x, y - 10), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 0.7, color = (0, 0, 255), thickness = 1)

# Display the image to our screen
cv2.imshow(windowName, image)

# Wait for a key press to finish program
cv2.waitKey(0)

# Any open window created by OpenCV are closed
cv2.destroyAllWindows()