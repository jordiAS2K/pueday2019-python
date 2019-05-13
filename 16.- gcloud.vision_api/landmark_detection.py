# Doc: https://cloud.google.com/vision/
# La API Cloud Vision utiliza modelos ya preparados y permite crear modelos personalizados y flexibles que se adaptan a 
# cada caso práctico a través de AutoML Vision.
# 
# Usage:
# python landmark_detection.py --image resources/notre-dame.jpg --full
# python landmark_detection.py --image resources/notre-dame-2.jpeg --full
# python landmark_detection.py --image resources/puerta-del-sol.jpg --full
# python landmark_detection.py --image resources/cibeles.jpg --full

# Import the necessary packages
import io
import os
from google.cloud import vision
from google.cloud.vision import types
import argparse
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to where the image file resides")
ap.add_argument("-f", "--full", required = False, action='store_true', help = "use full screen mode")
args = vars(ap.parse_args())

# The Google Cloud Vision API allows developers to easily integrate vision detection features within applications, 
# including image labeling, face and landmark detection, optical character recognition (OCR), and tagging of explicit content.

# Authenticate API requests
# Set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the file path of the JSON file that contains your service account key.
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "credentials/credentials.json"

# Configure windows
windowName = "Google Cloud Vision API"
if (args["full"]):
    cv2.namedWindow(windowName, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# The name of the image file to annotate
# os.path.dirname(__file__): absolute dir the script is in
filename = os.path.join(os.path.dirname(__file__), args["image"])

# Loads the image into memory
with io.open(filename, 'rb') as file:
    content = file.read()

# Load image in memory
img = cv2.imread(filename)
cv2.imshow(windowName, img)

# Wait until press a key
cv2.waitKey(0)

# Instantiates a client
client = vision.ImageAnnotatorClient()
image = types.Image(content = content)

# Performs lanmark detection on the image file
# Docu: https://cloud.google.com/vision/docs/detecting-landmarks#vision-landmark-detection-protocol
response = client.landmark_detection(image)

# Process the response
landmarks  = response.landmark_annotations

print(landmarks)
for landmark in landmarks:
    print("-------------------------------------------------")
    print(f"Description: {landmark.description}")
    print(f"Score: {landmark.score}")
    print("-------------------------------------------------")

    if (landmark.score > 0.5):
        points = []
        for point in landmark.bounding_poly.vertices:
            points.append((point.x,point.y))
        
        cv2.rectangle(img, pt1 = points[0], pt2 = points[2], color = (0,255,0), thickness = 2)
        cv2.rectangle(img, pt1 = points[0], pt2 = (points[2][0], points[0][1] + 30), color = (0,255,0), thickness = -1)
        cv2.putText(img, text = landmark.description, org = (points[0][0] + 5, points[0][1] + 25), fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0, 0, 0), thickness = 1)
        
cv2.imshow(windowName, img)

cv2.waitKey(0)


